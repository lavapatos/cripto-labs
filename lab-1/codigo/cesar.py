import sys

if len(sys.argv) != 3:
    print(f'Uso: python3 {sys.argv[0]} "texto" corrimiento')
    sys.exit(1)

texto = sys.argv[1]

try:
    corrimiento = int(sys.argv[2])
except ValueError:
    print("Error: el corrimiento debe ser un número entero.")
    sys.exit(1)

resultado = ""

for caracter in texto:
    if "a" <= caracter <= "z":
        resultado += chr((ord(caracter) - ord("a") + corrimiento) % 26 + ord("a"))
    elif "A" <= caracter <= "Z":
        resultado += chr((ord(caracter) - ord("A") + corrimiento) % 26 + ord("A"))
    else:
        resultado += caracter

print(resultado)