/**
 * api.js — Shim que reemplaza window.pywebview.api por llamadas fetch al servidor Flask.
 */

(function () {
    "use strict";

    const SESSION_MINUTOS = 5;
    const paginasPublicas = ["/", "/login"];
    const enPaginaPublica = paginasPublicas.includes(window.location.pathname);

    /* ── Sesión expirada: redirige al login con parámetro ─── */
    function manejarExpiracion() {
        sessionStorage.clear();
        localStorage.removeItem("rolUsuario");
        localStorage.removeItem("usuarioLogueado");
        // Redirigir limpiamente sin overlay que bloquee
        window.location.href = "/?expired=1";
    }

    /* ── Llamada genérica a la API ───────────────────────── */
    async function llamarAPI(metodo, args) {
        try {
            const resp = await fetch(`/api/${metodo}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ args: args })
            });

            if (resp.status === 401) {
                if (!enPaginaPublica) manejarExpiracion();
                return null;
            }

            return await resp.json();
        } catch (err) {
            console.error(`[api.js] Error en ${metodo}:`, err);
            throw err;
        }
    }

    /* ── Proxy ───────────────────────────────────────────── */
    const apiProxy = new Proxy({}, {
        get(_, metodo) {
            return (...args) => llamarAPI(metodo, args);
        }
    });

    window.pywebview = { api: apiProxy };

    /* ── Disparar pywebviewready al cargar el DOM ─────────── */
    function dispararReady() {
        window.dispatchEvent(new CustomEvent("pywebviewready"));
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", dispararReady);
    } else {
        setTimeout(dispararReady, 0);
    }

    /* ── En páginas protegidas: verificar sesión al cargar ── */
    if (!enPaginaPublica) {
        fetch("/api/check_auth", { credentials: "include" })
            .then(r => { if (r.status === 401) manejarExpiracion(); })
            .catch(() => {});
    }

    console.log("[api.js] cargado — sesión: %d min", SESSION_MINUTOS);
})();
