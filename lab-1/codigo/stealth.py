import os
import sys
import time
import secrets
import struct

from scapy.all import IP, ICMP, Raw, send


if len(sys.argv) != 2:
    print(f'Uso: sudo python3 {sys.argv[0]} "texto"')
    sys.exit(1)

texto = sys.argv[1]
destino = "127.0.0.1"

identifier = os.getpid() & 0xFFFF
ip_id_inicial = secrets.randbelow(0x10000)

for seq, caracter in enumerate(texto, start=1):
    valor = ord(caracter)
    if valor > 0xFF:
        print(f"Error: el carácter {caracter!r} no cabe en un solo byte.")
        sys.exit(1)

    ahora = time.time()
    segundos = int(ahora)
    microsegundos = int((ahora - segundos) * 1_000_000)

    # Linux ping en x86_64 coloca tv_sec como 8 bytes little-endian.
    timestamp = struct.pack("<Q", segundos)

    # Wireshark deja tv_usec dentro de Data: se reemplaza su primer byte
    # por el carácter y se conservan los dos bytes siguientes del valor real.
    usec_bytes = microsegundos.to_bytes(8, "little")
    data_inicial = bytes([valor]) + usec_bytes[1:3] + b"\x00" * 5

    # Patrón fijo de 40 bytes: 0x10, 0x11, ..., 0x37.
    patron = bytes(range(0x10, 0x38))

    payload = timestamp + data_inicial + patron

    paquete = (
        IP(
            src="127.0.0.1",
            dst=destino,
            ttl=64,
            flags="DF",
            id=(ip_id_inicial + seq - 1) & 0xFFFF,
        )
        / ICMP(
            type=8,
            code=0,
            id=identifier,
            seq=seq & 0xFFFF,
        )
        / Raw(load=payload)
    )

    send(paquete, verbose=False)
    print(f"seq={seq} caracter={caracter!r}")

    if seq != len(texto):
        time.sleep(1)