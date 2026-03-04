const toggle = document.getElementById("sidebarToggle");

function adjustSidebar() {
    if (window.innerWidth < 992) {
        document.body.classList.add("sidebar-collapsed");
    }
}

if (toggle) {
    toggle.addEventListener("click", function () {
        document.body.classList.toggle("sidebar-collapsed");
    });
}

// close sidebar when clicking outside on narrow screens
document.addEventListener('click', function (e) {
    if (window.innerWidth < 992 && !document.body.classList.contains('sidebar-collapsed')) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
            document.body.classList.add('sidebar-collapsed');
        }
    }
});

window.addEventListener('resize', adjustSidebar);
window.addEventListener('DOMContentLoaded', adjustSidebar);
