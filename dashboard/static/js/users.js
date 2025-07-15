document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("customDropdownToggle");
    const menu = document.getElementById("customDropdownMenu");

    toggleBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        menu.classList.toggle("show");
    });

    document.addEventListener("click", function (e) {
        if (!menu.contains(e.target) && !toggleBtn.contains(e.target)) {
            menu.classList.remove("show");
        }
    });
});
