# Laboratorio 1

Canal encubierto sobre tráfico ICMP. El mensaje se cifra con César, se envía usando un carácter por echo request y luego se recupera desde una captura de wireshark.

Los tres programas fueron generados con ChatGPT, tal como exige la actividad. Las ejecuciones, capturas y comprobaciones se hicieron de forma local.

## Contenido

- `codigo/`: versiones finales de `cesar.py`, `stealth.py` y `mitm.py`.
- `pcaps/`: captura completa con los ping de comparación y captura que contiene solamente el mensaje.
- `capturas/`: imágenes utilizadas en el informe.
- `prompts/`: texto de los siete mensajes entregados a ChatGPT.
- `informe/`: fuente TEX, PDF y recortes del enunciado usados en el documento.

## Requisitos

- Python 3
- Scapy
- Permisos para enviar paquetes ICMP
- Wireshark o TShark para revisar los pcap

## Ejecución

```bash
python3 codigo/cesar.py "criptografia y seguridad en redes" 9
sudo python3 codigo/stealth.py "larycxpajorj h bnpdarmjm nw anmnb"
python3 codigo/mitm.py pcaps/stealth_solo.pcapng
```

`stealth.py` tiene el origen y el destino fijados en `127.0.0.1`.
