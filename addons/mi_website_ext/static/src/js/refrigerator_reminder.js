/** @odoo-module **/
import { browser } from "@web/core/browser/browser";

const checkRefrigeratorReminder = () => {
    const intranetContainer = document.getElementById("wrapwrap");
    if (!intranetContainer) {
        return; 
    }

    if (window.location.pathname.includes("/web/login")) {
        return;
    }

    const now = new Date();
    const dayOfWeek = now.getDay(); 
    const hour = now.getHours();

    if (dayOfWeek === 5 && hour >= 12) {
        const todayKey = "refrigerator_read_" + now.toISOString().split("T")[0];
        const alreadyRead = browser.localStorage.getItem(todayKey);

        if (!alreadyRead) {
            const popup = document.getElementById("refrigerator_reminder_popup");
            const btn = document.getElementById("btn_read_refrigerator");

            if (popup && btn) {
                popup.classList.add("show-popup");

                btn.onclick = () => {
                    browser.localStorage.setItem(todayKey, "true");
                    popup.classList.remove("show-popup");
                };
            } else {
                setTimeout(checkRefrigeratorReminder, 1000);
            }
        }
    }
};

// Iniciamos la ejecución con un ligero delay para que el DOM esté listo
setTimeout(checkRefrigeratorReminder, 2000);