from .crc import calcular_crc_manual


POLYNOMIOS = {
    "MODBUS":       "11000000000000101",  # x^16 + x^15 + x^2 + 1
    "ARC":          "10001000000100001",  # x^16 + x^12 + x^5 + 1
    "MAXIM":        "10011000000010001",  # x^16 + x^15 + x^14 + x^11 + x^4 + x^2 + 1
    "CCITT_FALSE":  "10001000000100001"   # x^^16 + x^^12 + x^5 + 1 
}

def string_to_bits(s):
    return ''.join(f"{ord(c):08b}" for c in s)

def calcular_crc(nome, matricula):
    bits = string_to_bits(nome)

    print("========== MSG =========")
    print(bits)
    print("========== MSG =========")

    resultado = None
    if matricula[-1] in [0,1,2,3,4,5]:
        resultado = calcular_crc_manual(bits, POLYNOMIOS["MODBUS"])
    elif matricula[-1] in [6,7]:
        resultado = calcular_crc_manual(bits, POLYNOMIOS["MAXIM"])
    else:
        resultado = calcular_crc_manual(bits, POLYNOMIOS["CCITT_FALSE"])
    return resultado


nome = "Beatriz"
nome = nome.replace(" ", "")

matricula = "123110177"
resultado = calcular_crc(nome, matricula)

