from matplotlib import pyplot as plt

def calcula_media(vetor):
    soma = 0
    for num in vetor:
        soma += num
    return soma / len(vetor)

data = [
    {
        "tamanho": 1500,
        "tempo_manual": 1.0353675830010616,
        "mem_pico_manual": 105.7509765625,
        "tempo_lib": 0.3620580089991563,
        "mem_pico_lib": 1.46875
    },
    {
        "tamanho": 3000,
        "tempo_manual": 2.1477182469971012,
        "mem_pico_manual": 211.2431640625,
        "tempo_lib": 0.7282995509995089,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 4500,
        "tempo_manual": 3.1501371760023176,
        "mem_pico_manual": 316.7119140625,
        "tempo_lib": 1.074397645999852,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 6000,
        "tempo_manual": 4.200391148002382,
        "mem_pico_manual": 422.1806640625,
        "tempo_lib": 1.4308576329967764,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 7500,
        "tempo_manual": 5.232139138002822,
        "mem_pico_manual": 527.6494140625,
        "tempo_lib": 1.791425966002862,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 9000,
        "tempo_manual": 6.38168229400253,
        "mem_pico_manual": 633.1181640625,
        "tempo_lib": 2.1431724350004515,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 10500,
        "tempo_manual": 7.291989080000349,
        "mem_pico_manual": 738.5869140625,
        "tempo_lib": 2.488021460998425,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 12000,
        "tempo_manual": 8.385831932999281,
        "mem_pico_manual": 844.0556640625,
        "tempo_lib": 2.873387923998962,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 13500,
        "tempo_manual": 9.57971223399727,
        "mem_pico_manual": 949.5244140625,
        "tempo_lib": 3.2670976300032635,
        "mem_pico_lib": 1.2421875
    },
    {
        "tamanho": 15000,
        "tempo_manual": 10.72720446999665,
        "mem_pico_manual": 1054.9931640625,
        "tempo_lib": 3.6353538049988856,
        "mem_pico_lib": 1.2421875
    }
]

x = [item["tamanho"] for item in data]
y1 = [item["tempo_manual"] for item in data]
y2 = [item["tempo_lib"] for item in data]
y3 = [item["mem_pico_manual"] for item in data]
y4 = [item["mem_pico_lib"] for item in data]


plt.plot(x, y1, marker='o')
plt.xlabel("Tamanho em Bytes")
plt.ylabel("Tempo Manual (s)")
plt.title("Tamanho vs Tempo Manual")
plt.grid(True)
plt.show()

plt.plot(x, y2, marker='o')
plt.xlabel("Tamanho em Bytes")
plt.ylabel("Tempo Lib (s)")
plt.title("Tamanho vs Tempo Lib")
plt.grid(True)
plt.show()

plt.plot(x, y3, marker='o')
plt.xlabel("Tamanho em Bytes")
plt.ylabel("Pico máximo de memória crc manaul (Kb)")
plt.title("Tamanho vs Pico de memória crc manual")
plt.grid(True)
plt.show()


plt.plot(x, y4, marker='o')
plt.xlabel("Tamanho em Bytes")
plt.ylabel("Pico máximo de memória crc lib (Kb)")
plt.title("Tamanho vs Pico de memória crc lib")
plt.grid(True)
plt.show()

coeficientes_mem_manual = []
coeficientes_mem_lib = []
coeficientes_time_manual = []
coeficientes_time_lib = []

for i in range(len(data)-1):
    x1 = data[i]['tamanho']
    x2 = data[i+1]['tamanho']

    y1_mem_manual = data[i]['mem_pico_manual']
    y2_mem_manual = data[i+1]['mem_pico_manual']

    y1_mem_lib = data[i]['mem_pico_lib']
    y2_mem_lib = data[i+1]['mem_pico_lib']

    y1_time_manual = data[i]['tempo_manual']
    y2_time_manual = data[i+1]['tempo_manual']

    y1_time_lib = data[i]['tempo_lib']
    y2_time_lib = data[i+1]['tempo_lib']

    coeficiente_mem_manual = (y2_mem_manual - y1_mem_manual) / (x2 - x1)
    coeficiente_mem_lib = (y2_mem_lib - y1_mem_lib) / (x2 - x1)
    coeficiente_time_manual = (y2_time_manual - y1_time_manual) / (x2 - x1)
    coeficiente_time_lib = (y2_time_lib - y1_time_lib) / (x2 - x1)

    coeficientes_mem_manual.append(coeficiente_mem_manual)
    coeficientes_mem_lib.append(coeficiente_mem_lib)
    coeficientes_time_manual.append(coeficiente_time_manual)
    coeficientes_time_lib.append(coeficiente_time_lib)
    
for i in range(len(coeficientes_time_lib)):
    ca_mem_manual = calcula_media(coeficientes_mem_manual)
    ca_mem_lib = calcula_media(coeficientes_mem_lib)
    ca_time_manual = calcula_media(coeficientes_time_manual)
    ca_time_lib = calcula_media(coeficientes_time_lib)

print(coeficientes_mem_manual)
print(coeficientes_mem_lib)
print(coeficientes_time_manual)
print(coeficientes_time_lib)
print(ca_time_lib)