/* ---------- DOM CACHE ---------- */

const lastUpdated = document.getElementById('last-updated');

const mtbfValue = document.getElementById('mtbf-value');
const mttrValue = document.getElementById('mttr-value');
const availabilityValue = document.getElementById('availability-value');
const alertsValue = document.getElementById('alerts-value');

const equipmentTableBody = document.getElementById('equipment-table-body');
const alertsContainer = document.getElementById('alerts-container');


/* ---------- INIT ---------- */

document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
    setInterval(refreshData, 30000);
});


function initDashboard() {
    loadMetrics();
    loadEquipment();
    loadAlerts();
    updateTimestamp();
}


/* ---------- REFRESH ---------- */

function refreshData() {

    Promise.all([
        loadMetrics(),
        loadEquipment(),
        loadAlerts()
    ]).then(updateTimestamp);

}


/* ---------- TIME ---------- */

function updateTimestamp() {
    if (lastUpdated) {
        lastUpdated.textContent = new Date().toLocaleTimeString();
    }
}


/* ---------- FETCH HELPER ---------- */

async function fetchJSON(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`API error: ${url}`);
    return response.json();
}


/* ---------- METRICS ---------- */

async function loadMetrics() {

    try {

        const data = await fetchJSON('/api/metrics');

        mtbfValue.textContent = data.mtbf || '--';
        mttrValue.textContent = data.mttr || '--';
        availabilityValue.textContent = (data.availability || '--') + '%';
        alertsValue.textContent = data.active_alerts || '--';

    } catch (error) {
        console.error('Metrics error:', error);
    }

}


/* ---------- EQUIPMENT ---------- */

async function loadEquipment() {

    try {

        const data = await fetchJSON('/api/equipment');

        let html = '';

        for (const item of data) {

            html += `
            <tr class="hover:bg-slate-800 transition-colors">

                <td class="p-3 font-mono text-blue-400">${item.id}</td>

                <td class="p-3 text-white">${item.name}</td>

                <td class="p-3">
                    <span class="px-2 py-1 rounded-full text-xs font-medium ${getStatusClass(item.status)}">
                        ${item.status.toUpperCase()}
                    </span>
                </td>

                <td class="p-3 text-slate-400">${item.last_failure}</td>

                <td class="p-3 text-slate-400 text-sm">${item.last_updated}</td>

            </tr>
            `;
        }

        equipmentTableBody.innerHTML = html;

    } catch (error) {
        console.error('Equipment error:', error);
    }

}


function getStatusClass(status) {

    switch (status.toLowerCase()) {

        case 'operational':
            return 'bg-green-500/20 text-green-400';

        case 'critical':
            return 'bg-red-500/20 text-red-400';

        case 'maintenance':
            return 'bg-amber-500/20 text-amber-400';

        default:
            return 'bg-slate-500/20 text-slate-400';

    }

}


/* ---------- ALERTS ---------- */

async function loadAlerts() {

    try {

        const data = await fetchJSON('/api/alerts');

        if (!data.length) {

            alertsContainer.innerHTML =
                `<div class="p-4 bg-slate-800 rounded-lg text-center text-slate-400">
                    No active alerts
                </div>`;

            return;
        }

        let html = '';

        for (const alert of data) {

            html += `
            <div class="bg-slate-800 p-4 rounded-lg">

                <div class="flex items-start gap-3">

                    <i data-lucide="alert-circle"
                    class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5"></i>

                    <div>

                        <p class="text-white font-medium text-sm">
                        ${alert.equipment}
                        </p>

                        <p class="text-red-400 text-sm mt-1">
                        ${alert.message}
                        </p>

                        <p class="text-slate-500 text-xs mt-2">
                        ${alert.time}
                        </p>

                    </div>

                </div>

            </div>
            `;
        }

        alertsContainer.innerHTML = html;

        if (window.lucide) lucide.createIcons();

    } catch (error) {
        console.error('Alerts error:', error);
    }

}