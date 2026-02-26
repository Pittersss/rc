# -*- coding: utf-8 -*-

import csv
import json
import threading
import time
import copy
from argparse import ArgumentParser

import requests
from flask import Flask, jsonify, request

class Router:
    """
    Representa um roteador que executa o algoritmo de Vetor de Distância.
    """

    def __init__(self, my_address, neighbors, my_network, update_interval=1):
        """
        Inicializa o roteador.

        :param my_address: O endereço (ip:porta) deste roteador.
        :param neighbors: Um dicionário contendo os vizinhos diretos e o custo do link.
                          Ex: {'127.0.0.1:5001': 5, '127.0.0.1:5002': 10}
        :param my_network: A rede que este roteador administra diretamente.
                           Ex: '10.0.1.0/24'
        :param update_interval: O intervalo em segundos para enviar atualizações, o tempo que o roteador espera 
                                antes de enviar atualizações para os vizinhos.        """
        self.my_address = my_address
        self.neighbors = neighbors
        self.my_network = my_network
        self.update_interval = update_interval

        self.routing_table = {}

        #Rota para rede que este roteador administra
        self.routing_table[self.my_network] = {
            'cost': 0, 
            'next_hop': str(self.my_network)
        }

        #Rotas para os vizinhos (Lembrar de olhar com calma a questão de redes com mais de uma porta)
        
        print("Tabela de roteamento inicial:")
        print(json.dumps(self.routing_table, indent=4))

        # Inicia o processo de atualização periódica em uma thread separada
        self._start_periodic_updates()

    def _start_periodic_updates(self):
        """Inicia uma thread para enviar atualizações periodicamente."""
        thread = threading.Thread(target=self._periodic_update_loop)
        thread.daemon = True
        thread.start()

    def _periodic_update_loop(self):
        """Loop que envia atualizações de roteamento em intervalos regulares."""
        while True:
            time.sleep(self.update_interval)
            print(f"[{time.ctime()}] Enviando atualizações periódicas para os vizinhos...")
            try:
                self.send_updates_to_neighbors()
            except Exception as e:
                print(f"Erro durante a atualização periódida: {e}")

    def send_updates_to_neighbors(self):
        """
        Envia a tabela de roteamento (potencialmente sumarizada) para todos os vizinhos.
        """
        # TODO: O código abaixo envia a tabela de roteamento *diretamente*.
        #
        # ESTE TRECHO DEVE SER CHAMAADO APOS A SUMARIZAÇÃO.
        #
        # dica:
        # 1. CRIE UMA CÓPIA da `self.routing_table` NÃO ALTERE ESTA VALOR.
        # 2. IMPLEMENTE A LÓGICA DE SUMARIZAÇÃO nesta cópia.
        # 3. ENVIE A CÓPIA SUMARIZADA no payload, em vez da tabela original.

            
        tabela_para_enviar = copy.deepcopy(self.routing_table)

        mudou = True
        while mudou:
            mudou = False
            
            destinos = list(tabela_para_enviar.keys())       

            for i in range(len(destinos)):
                for j in range(i + 1, len(destinos)):
                    d1 = destinos[i]
                    d2 = destinos[j]
                    
                    r1 = tabela_para_enviar[d1]
                    r2 = tabela_para_enviar[d2]
                    
                    if r1["next_hop"] != r2["next_hop"]: continue

                    if can_aggregate(d1, d2):
                        agregada = aggregate(d1, d2)
                        novo_custo = max(r1["cost"], r2["cost"])

                        del tabela_para_enviar[d1]
                        del tabela_para_enviar[d2]

                        tabela_para_enviar[agregada] = {
                            "cost": novo_custo,
                            "next_hop": r1["next_hop"]
                        }

                        mudou = True
                        break
                if mudou:
                    break

                        
        payload = {
            "sender_address": self.my_address,
            "routing_table": tabela_para_enviar
        }

        for neighbor_address in self.neighbors:
            url = f'http://{neighbor_address}/receive_update'
            try:
                print(f"Enviando tabela para {neighbor_address}")
                requests.post(url, json=payload, timeout=5)
            except requests.exceptions.RequestException as e:
                print(f"Não foi possível conectar ao vizinho {neighbor_address}. Erro: {e}")

def ip_to_int(ip):
    parts = ip.split(".")
    return (int(parts[0]) << 24) | \
           (int(parts[1]) << 16) | \
           (int(parts[2]) << 8)  | \
           int(parts[3])

def int_to_ip(num):
    return ".".join([
        str((num >> 24) & 255),
        str((num >> 16) & 255),
        str((num >> 8) & 255),
        str(num & 255)
    ])

def can_aggregate(net1, net2):
    ip1, prefix1 = net1.split("/")
    ip2, prefix2 = net2.split("/")

    prefix1 = int(prefix1)
    prefix2 = int(prefix2)


    if prefix1 != prefix2: return False

    size = 2 ** (32 - prefix1)

    int1 = ip_to_int(ip1)
    int2 = ip_to_int(ip2)

    if abs(int1 - int2) != size: return False

    lower = min(int1, int2)
    super_prefix = prefix1 - 1
    super_size = 2 ** (32 - super_prefix)

    return (lower % super_size) == 0

def aggregate(net1, net2):
    ip1, prefix = net1.split("/")
    prefix = int(prefix)

    int1 = ip_to_int(ip1)

    super_prefix = prefix - 1
    super_size = 2 ** (32 - super_prefix)

    super_network_int = (int1 // super_size) * super_size

    super_ip = int_to_ip(super_network_int)

    return f"{super_ip}/{super_prefix}"

# --- API Endpoints ---
# Instância do Flask e do Roteador (serão inicializadas no main)
app = Flask(__name__)
router_instance = None

@app.route('/routes', methods=['GET'])
def get_routes():
    """Endpoint para visualizar a tabela de roteamento atual."""
   
    if router_instance:
        return jsonify({
            "vizinhos" : router_instance.neighbors,
            "my_network": router_instance.my_network,
            "my_address": router_instance.my_address,
            "update_interval": router_instance.update_interval,
            "routing_table": router_instance.routing_table # Exibe a tabela de roteamento atual (a ser implementada)
        })
    return jsonify({"error": "Roteador não inicializado"}), 500


@app.route('/receive_update', methods=['POST'])
def receive_update():
    """Endpoint que recebe atualizações de roteamento de um vizinho."""
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400

    update_data = request.json
    sender_address = update_data.get("sender_address")
    sender_table = update_data.get("routing_table")

    if not sender_address or not isinstance(sender_table, dict):
        return jsonify({"error": "Missing sender_address or routing_table"}), 400

    if sender_address not in router_instance.neighbors:
        return jsonify({"error": "Sender adress is not in my neighbor list"}), 400

    print(f"Recebida atualização de {sender_address}:")
    print(json.dumps(sender_table, indent=4))

    cost_sender = router_instance.neighbors[sender_address]

    table_changed = False

    for network, info in sender_table.items():
        new_cost = cost_sender + info['cost']
        if network not in router_instance.routing_table:
            router_instance.routing_table[network] = {'cost': new_cost, 'next_hop': sender_address}
            table_changed = True
        else:
            current_route = router_instance.routing_table[network]
            if current_route['next_hop'] == sender_address and current_route['cost'] != new_cost:
                router_instance.routing_table[network]['cost'] = new_cost
                table_changed = True

            elif current_route['cost'] > new_cost:
                router_instance.routing_table[network] = {'cost': new_cost, 'next_hop': sender_address}
                table_changed = True

    if table_changed:
        print(f'Tabela de roteamento do roteador com endereço {router_instance.my_address} mudou!')
        print(router_instance.routing_table)

    return jsonify({"status": "success", "message": "Update received"}), 200


if __name__ == '__main__':
    parser = ArgumentParser(description="Simulador de Roteador com Vetor de Distância")
    parser.add_argument('-p', '--port', type=int, default=5000, help="Porta para executar o roteador.")
    parser.add_argument('-f', '--file', type=str, required=True, help="Arquivo CSV de configuração de vizinhos.")
    parser.add_argument('--network', type=str, required=True, help="Rede administrada por este roteador (ex: 10.0.1.0/24).")
    parser.add_argument('--interval', type=int, default=10, help="Intervalo de atualização periódica em segundos.")
    parser.add_argument('-i', '--ip', default='127.0.0.1', help='IP para bind do servidor')
    args = parser.parse_args()

    # Leitura do arquivo de configuração de vizinhos
    neighbors_config = {}
    try:
        with open(args.file, mode='r') as infile:
            reader = csv.DictReader(infile)
            print("Colunas detectadas:", reader.fieldnames)
            for row in reader:
                neighbors_config[row['vizinho']] = int(row['custo'])
    except FileNotFoundError:
        print(f"Erro: Arquivo de configuração '{args.file}' não encontrado.")
        exit(1)
    except (KeyError, ValueError) as e:
        print(f"Erro no formato do arquivo CSV: {e}. Verifique as colunas 'vizinho' e 'custo'.")
        exit(1)

    my_full_address = f"{args.ip}:{args.port}"
    print("--- Iniciando Roteador ---")
    print(f"Endereço: {my_full_address}")
    print(f"Rede Local: {args.network}")
    print(f"Vizinhos Diretos: {neighbors_config}")
    print(f"Intervalo de Atualização: {args.interval}s")
    print("--------------------------")

    router_instance = Router(
        my_address=my_full_address,
        neighbors=neighbors_config,
        my_network=args.network,
        update_interval=args.interval
    )

    # Inicia o servidor Flask
    app.run(host=args.ip, port=args.port, debug=False)