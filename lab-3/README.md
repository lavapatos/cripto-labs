# Laboratorio 3

Análisis del tratamiento de la contraseña en el registro y el inicio de sesión de MEGA,
realizado con una cuenta exclusiva del laboratorio. El informe documenta la derivación
PBKDF2 de MEGA v2, la observación del tráfico con DevTools y Burp Suite, una comparación
local del valor `uh` y la revisión de las políticas oficiales.

## Contenido

- `evidencias/capturas_informe/`: imágenes saneadas utilizadas en el informe.
- `scripts/`: código ejecutado localmente para comparar el valor derivado con `uh`.

El informe se entrega por separado y no se versiona en este repositorio.

## Procedencia del verificador

El archivo `scripts/A3_verificar_pbkdf2_login.js` reproduce mediante Web Crypto el
procedimiento descrito en el [MEGA Security
Whitepaper](https://mega.nz/SecurityWhitepaper.pdf) y en
[`js/security.js`](https://github.com/meganz/webclient/blob/master/js/security.js) del
cliente oficial. Compara el valor calculado localmente con `uh`; no forma parte del cliente
de MEGA ni realiza solicitudes de red.

Los HAR, las capturas originales y los valores de autenticación no se publican porque
contienen información sensible de la cuenta de laboratorio.
