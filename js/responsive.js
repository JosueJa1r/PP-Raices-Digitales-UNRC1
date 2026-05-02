// Toggle logic for responsive sidebars

function toggleSidebar(sidebarClass, activeClass = 'show-sidebar') {
    const sidebar = document.querySelector('.' + sidebarClass);
    if (!sidebar) return;
    
    // Toggle sidebar class
    sidebar.classList.toggle(activeClass);
    
    // Toggle overlay
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        overlay.onclick = closeSidebars;
        document.body.appendChild(overlay);
    }
    
    if (sidebar.classList.contains(activeClass)) {
        overlay.classList.add('show');
    } else {
        overlay.classList.remove('show');
    }
}

function closeSidebars() {
    const sidebars = document.querySelectorAll('.left-sidebar, .right-panel, .filters-sidebar, .right-sidebar');
    sidebars.forEach(sidebar => {
        sidebar.classList.remove('show-sidebar');
        sidebar.classList.remove('show-panel');
    });
    
    const overlay = document.querySelector('.sidebar-overlay');
    if (overlay) {
        overlay.classList.remove('show');
    }
}

// Toggle logic for dropdown menus
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// Close dropdown if clicked outside
window.addEventListener('click', function(e) {
    if (!e.target.closest('.user-profile')) {
        const dropdown = document.getElementById('user-dropdown');
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
});
