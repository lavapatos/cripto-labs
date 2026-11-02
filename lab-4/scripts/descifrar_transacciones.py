from pathlib import Path

from scapy.all import TCP, rdpcap
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


pcap = Path("documentos_lab/captura_y_claves_originales/transacciones_cifradas.pcap")
clave_pem = Path("documentos_lab/captura_y_claves_originales/clave_privada.pem")

paquetes = rdpcap(str(pcap))
payloads = []

for numero, paquete in enumerate(paquetes, 1):
    if TCP in paquete:
        payloads.append((numero, bytes(paquete[TCP].payload)))

trama_rsa, datos_rsa = next(
    (numero, datos) for numero, datos in payloads if datos.startswith(b"RSA_PIN|")
)

paquetes_aes = [
    (numero, datos)
    for numero, datos in payloads
    if datos.startswith(b"AESGCM|")
]

salt = datos_rsa[8:24]
ciphertext_rsa = datos_rsa[24:]

clave_privada = serialization.load_pem_private_key(
    clave_pem.read_bytes(),
    password=None,
)

pin = clave_privada.decrypt(
    ciphertext_rsa,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

clave_aes = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
).derive(pin)

print(f"Trama RSA_PIN: {trama_rsa}")
print(f"Salt (16 bytes): {salt.hex()}")
print(f"Ciphertext RSA extraído: {len(ciphertext_rsa)} bytes")
print(f"Primeros 16 bytes: {ciphertext_rsa[:16].hex()}")
print(f"PIN recuperado con OAEP SHA-256: {pin.decode()}")
print("Scrypt: n=2**14, r=8, p=1, clave de 32 bytes")
print(f"Clave AES-256: {clave_aes.hex()}")
print(f"Paquetes AES-GCM: {len(paquetes_aes)}")

aesgcm = AESGCM(clave_aes)
autenticadas = 0

print("\nTransacciones recuperadas:")

for indice, (trama, datos) in enumerate(paquetes_aes, 1):
    cuerpo = datos[7:]
    nonce = cuerpo[:12]
    cifrado_y_tag = cuerpo[12:]
    ciphertext = cifrado_y_tag[:-16]
    tag = cifrado_y_tag[-16:]

    try:
        texto = aesgcm.decrypt(nonce, cifrado_y_tag, None).decode("utf-8")
    except InvalidTag:
        print(f"Trama {trama}: autenticidad inválida")
        continue

    campos = {}
    for parte in texto.split("|")[1:]:
        nombre, valor = parte.split("=", 1)
        campos[nombre] = valor

    if indice == 1:
        print(f"Nonce de ejemplo (12 bytes): {nonce.hex()}")
        print(f"Ciphertext de ejemplo: {len(ciphertext)} bytes")
        print(f"Tag de ejemplo (16 bytes): {tag.hex()}\n")

    print(
        f"{indice:02d}. ID: {campos['ID']} | "
        f"Remitente: {campos['DE']} | "
        f"Destinatario: {campos['A']} | "
        f"Monto: {campos['MONTO']}"
    )
    autenticadas += 1

print(f"\nAutenticidad AES-GCM verificada: {autenticadas}/{len(paquetes_aes)}")
