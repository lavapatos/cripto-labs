# Laboratorio 2

Fuerza bruta controlada sobre el formulario vulnerable de DVWA. La actividad se realizó
en un contenedor Docker local publicado en 127.0.0.1:6969. Se compararon las solicitudes
generadas con burp, curl e hydra mediante capturas de tráfico en wireshark.

## Contenido

- `capturas/`: imágenes utilizadas en el informe.
- `diccionarios/`: listas acotadas de usuarios y contraseñas de prueba.
- `pcaps/`: capturas de tráfico de burp, curl e hydra.
- `raw/`: comandos, respuestas HTML, registros y salidas originales.
- `informe/`: fuente TEX y PDF del informe.

## Requisitos

- Docker
- DVWA `vulnerables/web-dvwa`
- burp suite
- hydra
- curl
- wireshark

## Ejecución

```bash
docker run --pull=never --name dvwa-lab2 --restart=no -d \
  -p 127.0.0.1:6969:80 vulnerables/web-dvwa:latest
```

Después de iniciar el contenedor, se puede acceder a DVWA desde
`http://127.0.0.1:6969`.

El informe documenta la configuración del formulario, las pruebas con diccionarios
acotados y la comparación del tráfico capturado.
