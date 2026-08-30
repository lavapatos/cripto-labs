import math
import sys

from scapy.all import IP, ICMP, PcapNgReader


if len(sys.argv) != 2:
    print(f"Uso: python3 {sys.argv[0]} archivo.pcapng")
    sys.exit(1)

ruta = sys.argv[1]
bytes_texto = bytearray()

try:
    with PcapNgReader(ruta) as captura:
        for paquete in captura:
            if IP not in paquete or ICMP not in paquete:
                continue
            if paquete[ICMP].type != 8:
                continue

            raw_icmp = bytes(paquete[ICMP].payload)
            if len(raw_icmp) < 9:
                continue

            # En stealth.py los primeros 8 bytes son el timestamp;
            # el carácter ocupa el primer byte de la zona Data.
            bytes_texto.append(raw_icmp[8])
except (OSError, ValueError) as error:
    print(f"Error al leer {ruta}: {error}")
    sys.exit(1)

if not bytes_texto:
    print("No se encontraron ICMP Echo Request IPv4 con el formato esperado.")
    sys.exit(1)

texto_cifrado = bytes(bytes_texto).decode("latin-1")
print(f"Texto cifrado: {texto_cifrado}\n")

frecuencias = {
    "a": 12.53, "b": 1.42, "c": 4.68, "d": 5.86, "e": 13.68,
    "f": 0.69, "g": 1.01, "h": 0.70, "i": 6.25, "j": 0.44,
    "k": 0.02, "l": 4.97, "m": 3.15, "n": 6.71, "o": 8.68,
    "p": 2.51, "q": 0.88, "r": 6.87, "s": 7.98, "t": 4.63,
    "u": 3.93, "v": 0.90, "w": 0.01, "x": 0.22, "y": 0.90,
    "z": 0.52,
}

palabras_comunes = {
    "de": 3.0, "la": 3.0, "el": 3.0, "en": 3.0, "y": 3.0,
    "que": 4.0, "los": 3.0, "las": 3.0, "un": 2.0, "una": 2.0,
    "por": 2.0, "para": 2.0, "con": 2.0, "del": 2.0, "al": 2.0,
    "se": 2.0, "es": 2.0,
}


def descifrar_cesar(texto, llave):
    resultado = []

    for caracter in texto:
        if "a" <= caracter <= "z":
            resultado.append(
                chr((ord(caracter) - ord("a") - llave) % 26 + ord("a"))
            )
        elif "A" <= caracter <= "Z":
            resultado.append(
                chr((ord(caracter) - ord("A") - llave) % 26 + ord("A"))
            )
        else:
            resultado.append(caracter)

    return "".join(resultado)


def puntuar_espanol(texto):
    letras = [
        caracter.lower()
        for caracter in texto
        if caracter.lower() in frecuencias
    ]

    if not letras:
        return float("-inf")

    # Log-verosimilitud según frecuencias de letras del español.
    puntaje = sum(
        math.log(frecuencias[letra] / 100.0)
        for letra in letras
    )

    # Bonificación independiente para palabras funcionales muy comunes.
    for palabra in texto.lower().split():
        puntaje += palabras_comunes.get(palabra, 0.0) * 2.5

    proporcion_vocales = sum(
        letra in "aeiou" for letra in letras
    ) / len(letras)

    # Penaliza distribuciones de vocales muy alejadas de un texto español normal.
    puntaje -= abs(proporcion_vocales - 0.45) * 12.0

    return puntaje


resultados = []

for llave in range(26):
    texto = descifrar_cesar(texto_cifrado, llave)
    puntaje = puntuar_espanol(texto)
    resultados.append((llave, puntaje, texto))

mejor_llave, mejor_puntaje, _ = max(resultados, key=lambda item: item[1])

print(
    "Puntaje: frecuencias de letras + palabras comunes "
    "+ cercanía a una proporción normal de vocales.\n"
)

VERDE = "\033[32m"
RESET = "\033[0m"

for llave, puntaje, texto in resultados:
    linea = f"llave {llave:2d} | puntaje {puntaje:8.2f} | {texto}"
    if llave == mejor_llave:
        print(f"{VERDE}{linea}{RESET}")
    else:
        print(linea)
