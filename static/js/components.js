async function loadSidebar() {

    const container = document.getElementById('sidebar-target');
    if (!container) return;

    try {

        const response = await fetch('/get_sidebar');
        if (!response.ok) throw new Error('Failed to fetch sidebar');

        container.innerHTML = await response.text();

        const currentPath = window.location.pathname;

        const links = container.querySelectorAll('.nav-item');

        for (const link of links) {

            if (link.getAttribute('href') === currentPath) {

                link.classList.add(
                    'bg-blue-600/20',
                    'text-white',
                    'border-l-4',
                    'border-blue-600'
                );

                link.classList.remove('text-slate-400');
            }
        }

        if (window.lucide) {
            lucide.createIcons();
        }

    } catch (error) {
        console.error('Sidebar load failed:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadSidebar);