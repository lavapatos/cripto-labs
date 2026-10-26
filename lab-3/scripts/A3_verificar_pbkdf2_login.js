/**
 * Laboratorio 3 - Verificación local de la derivación usada por MEGA v2.
 *
 * No envía solicitudes ni imprime contraseña, sal, clave derivada o `uh`.
 * Solo informa los parámetros empleados y si el valor calculado coincide
 * con el campo `uh` capturado durante un login propio autorizado.
 *
 * Fuentes:
 * - MEGA Security Whitepaper, 3.ª edición, pp. 19-20.
 * - https://github.com/meganz/webclient/blob/master/js/security.js
 */
(async () => {
    'use strict';

    const requestSecrets = () => new Promise((resolve, reject) => {
        document.getElementById('lab3-pbkdf2-dialog')?.remove();

        const dialog = document.createElement('dialog');
        dialog.id = 'lab3-pbkdf2-dialog';
        dialog.style.padding = '1.25rem';
        dialog.style.maxWidth = '34rem';

        const form = document.createElement('form');
        form.style.display = 'grid';
        form.style.gap = '0.75rem';

        const title = document.createElement('strong');
        title.textContent = 'Verificación local PBKDF2 de MEGA v2';
        form.append(title);

        const notice = document.createElement('span');
        notice.textContent = 'Los valores permanecerán ocultos y no serán enviados.';
        form.append(notice);

        const inputs = Object.create(null);
        const fields = [
            ['password', 'Contraseña exclusiva del laboratorio'],
            ['salt', 'Valor s de la respuesta us0'],
            ['expectedUh', 'Valor uh de la solicitud us']
        ];

        for (const [name, labelText] of fields) {
            const label = document.createElement('label');
            label.style.display = 'grid';
            label.style.gap = '0.25rem';
            label.textContent = labelText;

            const input = document.createElement('input');
            input.type = 'password';
            input.required = true;
            input.autocomplete = 'off';
            input.spellcheck = false;
            input.style.padding = '0.45rem';
            inputs[name] = input;

            label.append(input);
            form.append(label);
        }

        const controls = document.createElement('div');
        controls.style.display = 'flex';
        controls.style.gap = '0.5rem';
        controls.style.justifyContent = 'flex-end';

        const cancel = document.createElement('button');
        cancel.type = 'button';
        cancel.textContent = 'Cancelar';

        const verify = document.createElement('button');
        verify.type = 'submit';
        verify.textContent = 'Verificar localmente';

        controls.append(cancel, verify);
        form.append(controls);
        dialog.append(form);
        document.body.append(dialog);

        const finish = () => {
            dialog.close();
            dialog.remove();
        };

        cancel.addEventListener('click', () => {
            finish();
            reject(new Error('Verificación cancelada.'));
        }, {once: true});

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const values = {
                password: inputs.password.value,
                salt: inputs.salt.value.trim(),
                expectedUh: inputs.expectedUh.value.trim()
            };
            finish();
            resolve(values);
        }, {once: true});

        dialog.showModal();
        inputs.password.focus();
    });

    const base64UrlToBytes = (value) => {
        const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
        const padded = normalized + '='.repeat((4 - normalized.length % 4) % 4);
        const binary = window.atob(padded);
        return Uint8Array.from(binary, (character) => character.charCodeAt(0));
    };

    const bytesToBase64Url = (bytes) => {
        let binary = '';
        for (const byte of bytes) {
            binary += String.fromCharCode(byte);
        }
        return window.btoa(binary)
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=+$/u, '');
    };

    let secrets;
    let passwordBytes;
    let saltBytes;
    let expectedUhBytes;
    let derivedKeyBytes;

    try {
        secrets = await requestSecrets();
        saltBytes = base64UrlToBytes(secrets.salt);
        expectedUhBytes = base64UrlToBytes(secrets.expectedUh);

        if (saltBytes.length !== 32) {
            throw new Error(`La sal debe decodificar a 32 bytes; se obtuvieron ${saltBytes.length}.`);
        }
        if (expectedUhBytes.length !== 16) {
            throw new Error(`uh debe decodificar a 16 bytes; se obtuvieron ${expectedUhBytes.length}.`);
        }

        passwordBytes = new TextEncoder().encode(secrets.password);
        const keyMaterial = await window.crypto.subtle.importKey(
            'raw',
            passwordBytes,
            'PBKDF2',
            false,
            ['deriveBits']
        );

        const derivedBits = await window.crypto.subtle.deriveBits(
            {
                name: 'PBKDF2',
                hash: 'SHA-512',
                salt: saltBytes,
                iterations: 100000
            },
            keyMaterial,
            256
        );

        derivedKeyBytes = new Uint8Array(derivedBits);
        const calculatedUh = bytesToBase64Url(derivedKeyBytes.subarray(16, 32));
        const expectedUh = secrets.expectedUh.replace(/=+$/u, '');
        const matches = calculatedUh === expectedUh;

        const result = {
            Protocolo: 'MEGA v2',
            KDF: 'PBKDF2-HMAC-SHA-512',
            Iteraciones: 100000,
            'Sal decodificada': '256 bits',
            'Salida derivada': '256 bits',
            'Material enviado como uh': 'segundos 128 bits, Base64URL',
            'Coincide con el uh capturado': matches ? 'SÍ' : 'NO'
        };

        console.table(result);
        console.log(matches
            ? '[LAB3] RESULTADO: COINCIDE con el uh capturado.'
            : '[LAB3] RESULTADO: NO COINCIDE; revisar los tres datos sin efectuar otro login.');
    }
    catch (error) {
        console.error(`[LAB3] ${error.message}`);
    }
    finally {
        passwordBytes?.fill(0);
        saltBytes?.fill(0);
        expectedUhBytes?.fill(0);
        derivedKeyBytes?.fill(0);
        if (secrets) {
            secrets.password = '';
            secrets.salt = '';
            secrets.expectedUh = '';
        }
    }
})();
