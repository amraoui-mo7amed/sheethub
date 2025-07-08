
function toggleMenu(button) {
    const menu = button.nextElementSibling;
    // Close other open menus
    document.querySelectorAll('.dots-menu').forEach(m => {
        if (m !== menu) m.style.display = 'none';
    });

    // Toggle this one
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Close menu when clicking outside
document.addEventListener('click', function (e) {
    if (!e.target.closest('.product-card')) {
        document.querySelectorAll('.dots-menu').forEach(menu => {
            menu.style.display = 'none';
        });
    }
});
