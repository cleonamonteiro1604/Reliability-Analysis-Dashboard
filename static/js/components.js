// Function to dynamically load the sidebar into every page
async function loadSidebar() {

    // Find the HTML container where the sidebar should be injected
    const container = document.getElementById('sidebar-target');

    // If the container does not exist, stop execution
    if (!container) return;

    try {

        // Request sidebar HTML from the backend endpoint
        const response = await fetch('/get_sidebar');

        // If the request failed, throw an error
        if (!response.ok) throw new Error('Failed to fetch sidebar');

        // Insert the sidebar HTML into the container
        container.innerHTML = await response.text();

        // Get the current page path (example: /analysis)
        const currentPath = window.location.pathname;

        // Select all navigation links in the sidebar
        const links = container.querySelectorAll('.nav-item');

        // Loop through links to highlight the active page
        for (const link of links) {

            if (link.getAttribute('href') === currentPath) {

                // Add styles for the active link
                link.classList.add(
                    'bg-blue-600/20',
                    'text-white',
                    'border-l-4',
                    'border-blue-600'
                );

                // Remove inactive text style
                link.classList.remove('text-slate-400');
            }
        }

        // Re-render Lucide icons after HTML injection
        if (window.lucide) {
            lucide.createIcons();
        }

    } catch (error) {

        // Log any errors if sidebar loading fails
        console.error('Sidebar load failed:', error);
    }
}

// Run the sidebar loader once the page finishes loading
document.addEventListener('DOMContentLoaded', loadSidebar);