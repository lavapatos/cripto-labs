# Laboratorio 4

Configuración de un servidor SSH dentro de Docker y análisis de tráfico con Wireshark. La
segunda parte corresponde a la recuperación de transacciones protegidas con RSA-OAEP,
Scrypt y AES-GCM.

## Contenido

- [`informe/informe_lab4.pdf`](informe/informe_lab4.pdf): informe final.
- [`informe/informe_lab4.tex`](informe/informe_lab4.tex): fuente LaTeX del informe.
- [`configuracion/`](configuracion/): Dockerfile, configuración de `sshd` y clave pública
  autorizada para el cliente.
- [`scripts/descifrar_transacciones.py`](scripts/descifrar_transacciones.py): script usado
  para recuperar y presentar las transacciones.
- [`pcaps/ssh_local.pcapng`](pcaps/ssh_local.pcapng): captura local de la conexión SSH sobre
  la interfaz loopback.
- [`evidencias/capturas_informe/`](evidencias/capturas_informe/): capturas utilizadas como
  evidencia en el informe.

## Configuración SSH

Durante la prueba, el puerto 22 del contenedor se publicó solamente en
`127.0.0.1:22222`. El servidor se configuró para usar `curve25519-sha256`,
`aes256-ctr`, `hmac-sha2-256` y `ssh-ed25519`, junto con autenticación por clave pública.

## Script de descifrado

El script contiene el procedimiento utilizado para recuperar el PIN, derivar la clave
AES-256 y descifrar las transacciones. Para ejecutarlo se requieren Python 3, Scapy,
Cryptography, la captura y la clave privada RSA entregadas por el profesor. Estos dos últimos
archivos no se publican en el repositorio pero la url al drive están en el informe.

## Alcance

Las pruebas SSH se realizaron únicamente en localhost. La clave incluida en
`authorized_keys` es solamente la clave pública utilizada por el contenedor.
