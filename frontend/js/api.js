/**
 * api.js — Shim que reemplaza window.pywebview.api por llamadas fetch al servidor Flask.
 *
 * Uso: incluir ANTES de cualquier script que llame a window.pywebview.api.*
 *
 * Características:
 *  - Cada llamada window.pywebview.api.metodo(arg1, arg2) se convierte en
 *    POST /api/metodo  con body { args: [arg1, arg2] }
 *  - Si el servidor responde 401 (token expirado), redirige automáticamente al login.
 *  - El token JWT se maneja como httpOnly cookie (el servidor lo renueva en cada llamada).
 *  - window.pywebviewready se dispara automáticamente al cargar el DOM.
 */

(function () {
    "use strict";

    /* ── Sesión expirada ─────────────────────────────────── */
    function manejarExpiracion() {
        sessionStorage.clear();
        localStorage.removeItem("rolUsuario");
        localStorage.removeItem("usuarioLogueado");

        // Mostrar aviso antes de redirigir
        const aviso = document.createElement("div");
        aviso.style.cssText = [
            "position:fixed;top:0;left:0;width:100%;height:100%;",
            "background:rgba(0,0,0,0.7);display:flex;",
            "align-items:center;justify-content:center;z-index:99999"
        ].join("");
        aviso.innerHTML = `
            <div style="background:#fff;border-radius:16px;padding:40px;text-align:center;max-width:360px;">
                <div style="font-size:2.5rem;margin-bottom:12px;">⏰</div>
                <h2 style="color:#c0392b;margin-bottom:10px;">Sesión expirada</h2>
                <p style="color:#555;margin-bottom:20px;">
                    Tu sesión ha expirado por inactividad (${SESSION_MINUTOS} minutos).<br>
                    Por seguridad, inicia sesión nuevamente.
                </p>
                <button onclick="window.location.href='/'"
                    style="background:#2e7d32;color:#fff;border:none;border-radius:8px;
                           padding:12px 28px;font-size:1rem;cursor:pointer;">
                    Ir al Login
                </button>
            </div>`;
        document.body.appendChild(aviso);

        setTimeout(() => { window.location.href = "/"; }, 4000);
    }

    /* ── Llamada genérica a la API ───────────────────────── */
    const SESSION_MINUTOS = 5;

    async function llamarAPI(metodo, args) {
        try {
            const resp = await fetch(`/api/${metodo}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",           // envía la cookie JWT
                body: JSON.stringify({ args: args })
            });

            if (resp.status === 401) {
                manejarExpiracion();
                return null;
            }

            return await resp.json();
        } catch (err) {
            console.error(`[api.js] Error en ${metodo}:`, err);
            throw err;
        }
    }

    /* ── Proxy que intercepta cualquier propiedad de api ─── */
    const apiProxy = new Proxy({}, {
        get(_, metodo) {
            // Devuelve una función que acepta cualquier número de argumentos
            return (...args) => llamarAPI(metodo, args);
        }
    });

    /* ── Exponer como window.pywebview.api ───────────────── */
    window.pywebview = { api: apiProxy };

    /* ── Disparar 'pywebviewready' al cargar el DOM ──────── */
    function dispararReady() {
        const ev = new CustomEvent("pywebviewready");
        window.dispatchEvent(ev);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", dispararReady);
    } else {
        // DOM ya listo (script cargado tarde)
        setTimeout(dispararReady, 0);
    }

    /* ── Verificar autenticación al cargar cualquier página ─ */
    const paginasPublicas = ["/", "/login"];

    if (!paginasPublicas.includes(window.location.pathname)) {
        fetch("/api/check_auth", { credentials: "include" })
            .then(r => {
                if (r.status === 401) {
                    manejarExpiracion();
                }
            })
            .catch(() => {});
    }

    console.log("[api.js] Shim Analitic cargado — sesión: %d min", SESSION_MINUTOS);
})();
