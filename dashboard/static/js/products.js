document.addEventListener('DOMContentLoaded', function () {
    const additionalImagesToggle = document.getElementById('additionalImagesToggle');
    const additionalImagesDiv = document.getElementById('additionalImages');

    // Initialize visibility based on initial checkbox state
    if (additionalImagesDiv) {
        additionalImagesDiv.style.display = additionalImagesToggle.checked ? 'block' : 'none';

        // Add event listener for toggle changes
        additionalImagesToggle.addEventListener('change', function () {
            additionalImagesDiv.style.display = this.checked ? 'block' : 'none';
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const pixelToggle = document.getElementById("enablePixelSwitch");
    const pixelAsterisk = document.getElementById("pixelRequired");
    const additionalToggle = document.getElementById("additionalImagesToggle");
    const additionalAsterisk = document.getElementById("additionalImagesRequired");

    function togglePixelField() {
        if (pixelToggle && pixelAsterisk) {
            pixelAsterisk.style.display = pixelToggle.checked ? "inline" : "none";
        }
    }

    function toggleAdditionalImages() {
        if (additionalToggle && additionalAsterisk) {
            additionalAsterisk.style.display = additionalToggle.checked ? "inline" : "none";
        }
    }

    if (additionalToggle && additionalAsterisk) {
        additionalToggle.addEventListener("change", toggleAdditionalImages);
    }

    togglePixelField();
    toggleAdditionalImages();
});


// edit the product status 

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".change-status").forEach(function (el) {
        el.addEventListener("click", function (e) {
            e.preventDefault();

            const orderId = this.dataset.orderId;
            const newStatus = this.dataset.status;
            const updateUrl = this.dataset.updateUrl;

            fetch(updateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    order_id: orderId,
                    status: newStatus,
                }),
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            icon: 'success',
                            title: data.success_title,
                            text: data.message || 'Order status updated successfully.',
                            confirmButtonColor: '#3085d6',
                            timer: 1500,
                            showConfirmButton: false
                        }).then(() => {
                            location.reload();
                        });
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: data.message || 'An error occurred.',
                            confirmButtonColor: '#d33'
                        });
                    }
                })
                .catch(() => {
                    Swal.fire({
                        icon: 'error',
                        title: 'Request Failed',
                        text: 'Please check your internet connection or try again later.',
                        confirmButtonColor: '#d33'
                    });
                });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});



// Searching 
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("orderSearchInput");
    const timelineItems = document.querySelectorAll(".order-timeline .timeline-item");

    if (!searchInput || timelineItems.length === 0) return;

    searchInput.addEventListener("input", function () {
        const query = this.value.toLowerCase().trim();

        timelineItems.forEach(function (item) {
            const name = item.querySelector("h5")?.textContent.toLowerCase() || "";
            const email = item.querySelector(".fa-envelope")?.parentElement?.textContent.toLowerCase() || "";
            const phone = item.querySelector(".fa-phone")?.parentElement?.textContent.toLowerCase() || "";
            const orderId = item.dataset.orderId ? item.dataset.orderId.toLowerCase() : "";

            const matches =
                name.includes(query) ||
                email.includes(query) ||
                phone.includes(query) ||
                orderId.includes(query);

            // ⛔ OLD: item.classList.toggle("hidden", !matches);
            // ✅ NEW: toggle .hidden on parent .col-12
            const parent = item.closest(".col-6");
            if (parent) {
                parent.classList.toggle("hidden", !matches);
            }
        });
    });

    searchInput.addEventListener("blur", function () {
        if (!this.value.trim()) {
            timelineItems.forEach(item => {
                const parent = item.closest(".col-6");
                if (parent) parent.classList.remove("hidden");
            });
        }
    });
});
