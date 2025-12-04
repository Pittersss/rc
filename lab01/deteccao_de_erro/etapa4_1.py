import random
from .crc import calcular_crc_manual
from crc import Crc16, Calculator


POLYNOMIOS = {
    "MODBUS":       "11000000000000101",  # x^16 + x^15 + x^2 + 1
    "ARC":          "10001000000100001",  # x^16 + x^12 + x^5 + 1
    "MAXIM":        "10011000000010001",  # x^16 + x^15 + x^14 + x^11 + x^4 + x^2 + 1
    "CCITT_FALSE":  "10001000000100001"   # x^^16 + x^^12 + x^5 + 1 
}

def string_to_bits(s):
    return ''.join(f"{ord(c):08b}" for c in s)

def calcular_crc(MENSAGEM_BASE, matricula):
    bits = string_to_bits(MENSAGEM_BASE)

    print("========== MSG =========")
    print(bits)
    print("========== MSG =========")

    resultado = None
    if matricula[-1] in ["0","1","2","3","4","5"]:
        resultado = calcular_crc_manual(bits, POLYNOMIOS["MODBUS"])
    elif matricula[-1] in ["6","7"]:
        resultado = calcular_crc_manual(bits, POLYNOMIOS["MAXIM"])
    else:
        resultado = calcular_crc_manual(bits, POLYNOMIOS["CCITT_FALSE"])
    return resultado


def gerar_erro(quadro_len, n, pos):
    erro = ""
    for i in range(quadro_len):
        if pos <= i < pos + n:
            erro += "1"
        else:
            erro += "0"
    return erro

def xor_bits(quadro, erro):
    return ''.join(['1' if quadro[i] != erro[i] else '0' for i in range(len(quadro))])

def bits_to_bytes(bits):
    if len(bits) % 8 != 0:
        bits = bits.zfill(len(bits) + (8 - len(bits) % 8))

    byte_list = []
    for i in range(0, len(bits), 8):
        grupo = bits[i:i+8]
        byte_list.append(int(grupo, 2))  
    return bytes(byte_list)

def erro(MENSAGEM_BASE):
    resultados = []

    calculator_lib = Calculator(Crc16.MODBUS)
        
    crc_base = calcular_crc_manual(MENSAGEM_BASE, POLYNOMIOS["MODBUS"])
    quadro = MENSAGEM_BASE + crc_base

    for _ in range(10):
       
        n = random.randint(1, len(quadro))  
        pos = random.randint(0, len(quadro) - n)
        erro = gerar_erro(len(quadro), n, pos)
        quadro_corrompido = xor_bits(quadro, erro) 

        crc_m = calcular_crc_manual(quadro_corrompido, POLYNOMIOS["MODBUS"])

        quadro_bytes = bits_to_bytes(quadro_corrompido)

        crc_lib = format(calculator_lib.checksum(quadro_bytes), '016b')

        detectado_m = crc_m != "0"*16
        detectado_l = crc_lib != "0"*16

        resultados.append((erro, pos, n, detectado_m, detectado_l))
    
    return resultados

def print_resultados(resultados):
    i = 0
    for erro, pos, tamanho_erro, detectado_m, detectado_l in resultados:
        print(f"{'='*10} TESTE {i} {'='*10}")
        print(f"    ERRO = {erro} ")
        print(f"    POS = {pos} ")
        print(f"    TAMANHO_ERRO = {tamanho_erro} ")
        print(f"    DETECTADO PELO CRC MANUAL? = {detectado_m}")
        print(f"    DETECTADO PELO CRC LIB? = {detectado_l}")
        i+=1


    
MENSAGEM_BASE = "Beatriz"
MENSAGEM_BASE = MENSAGEM_BASE.replace(" ", "")

matricula = "123110177"
resultado = calcular_crc(MENSAGEM_BASE, matricula)
testes = erro(MENSAGEM_BASE)

print(resultado)

print_resultados(testes)


