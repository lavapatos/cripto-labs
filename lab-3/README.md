# Laboratorio 3

Análisis del tratamiento de la contraseña en el registro y el inicio de sesión de MEGA,
realizado con una cuenta creada exclusivamente para el laboratorio. Se revisó el tráfico con
DevTools y Burp Suite, se reprodujo localmente el cálculo de `uh` y se contrastaron los
resultados con la documentación y el código público de MEGA.

## Contenido

- [`informe/`](informe/): fuente TEX y PDF del informe.
- [`evidencias/capturas_informe/`](evidencias/capturas_informe/): nueve capturas saneadas
  utilizadas en el informe.
- [`scripts/A3_verificar_pbkdf2_login.js`](scripts/A3_verificar_pbkdf2_login.js): verificador
  local empleado para comparar el valor derivado con el `uh` observado.

Los HAR, las capturas originales y los valores de autenticación no se publican porque
contienen información sensible de la cuenta de laboratorio.

## Comprobación local

El verificador se preparó a partir del [MEGA Security
Whitepaper](https://mega.nz/SecurityWhitepaper.pdf) y de
[`js/security.js`](https://github.com/meganz/webclient/blob/master/js/security.js), donde se
describe e implementa el inicio de sesión de MEGA v2. El código usa Web Crypto para aplicar
PBKDF2-HMAC-SHA-512 con 100.000 iteraciones, toma los segundos 128 bits de la salida y los
compara con `uh` en Base64URL.

La ejecución se hizo desde la consola del navegador con la contraseña de la cuenta de prueba,
la sal devuelta por `us0` y el `uh` de la solicitud `us`. Los tres datos se ingresan en campos
ocultos. El script no realiza solicitudes de red ni imprime esos valores; solo muestra los
parámetros generales y si la comparación coincide.

## Alcance

Solo usé la cuenta que creé para el laboratorio. En Repeater reenvié una vez la solicitud
que ya había funcionado y paré cuando recibí la respuesta de la API. No abrí una sesión con
esa respuesta ni entré a ningún archivo.

De verdad no hice nada ilegal
