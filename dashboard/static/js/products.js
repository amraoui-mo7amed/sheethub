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


// Product Update 

const uploader = document.getElementById('customUploader');
const fileInput = document.getElementById('customInput');
const previewImage = document.getElementById('customPreview');

// Click to open file dialog
if (uploader) {
    uploader.addEventListener('click', () => fileInput.click());
    // Drag-over effect
    uploader.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploader.classList.add('dragover');
    });

    uploader.addEventListener('dragleave', () => {
        uploader.classList.remove('dragover');
    });

    uploader.addEventListener('drop', (e) => {
        e.preventDefault();
        uploader.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            fileInput.files = e.dataTransfer.files;
            preview(file);
        }
    });
}



// On file selected
if (fileInput) {
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file && file.type.startsWith('image/')) {
            preview(file);
        }
    });
}

function preview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
    };
    reader.readAsDataURL(file);
}


// Preview image 
document.addEventListener('DOMContentLoaded', () => {
    const uploadButtons = document.querySelectorAll('.upload-btn');

    uploadButtons.forEach(button => {
        const index = button.dataset.index;
        const fileInput = document.querySelector(`.file-input[data-index="${index}"]`);
        const imgPreview = document.querySelector(`.preview-img[data-index="${index}"]`);

        // Click upload button → open file dialog
        button.addEventListener('click', () => {
            fileInput.click();
        });

        // When file is selected → upload immediately
        fileInput.addEventListener('change', event => {
            const file = event.target.files[0];
            if (!file || !file.type.startsWith('image/')) {
                alert("Please select a valid image file.");
                return;
            }

            // Preview immediately
            const reader = new FileReader();
            reader.onload = e => {
                imgPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);

        });
    });

});


// Toggle Additional images update 
document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("productAllowAdditionalImages");
    const container = document.getElementById("previewImagesContainer");

    if (!checkbox || !container) return;

    const togglePreviewImageCards = () => {
        if (checkbox.checked) {
            container.classList.remove("d-none");
            container.classList.add("d-block");
        } else {
            container.classList.remove("d-block");
            container.classList.add("d-none");
        }
    };

    // Force re-check state on full load (useful if rendering is delayed)
    setTimeout(togglePreviewImageCards, 50);

    checkbox.addEventListener("change", togglePreviewImageCards);
});


//  JS to handle copy + feedback 
document.addEventListener("DOMContentLoaded", function () {
    const copyBtn = document.getElementById("copyProductUrlBtn");
    const urlInput = document.getElementById("productUrlInput");
    const copiedMsg = document.getElementById("copiedMsg");
    if (copyBtn) {

        copyBtn.addEventListener("click", function () {
            if (!urlInput) return;

            navigator.clipboard.writeText(urlInput.value)
                .then(() => {
                    // Show copied message
                    copiedMsg.classList.remove("d-none");

                    // Change bg to success
                    copyBtn.classList.remove("bg-primary");
                    copyBtn.classList.add("bg-success");

                    // Revert after 2 seconds
                    setTimeout(() => {
                        copiedMsg.classList.add("d-none");
                        copyBtn.classList.remove("bg-success");
                        copyBtn.classList.add("bg-primary");
                    }, 2000);
                })
                .catch((err) => {
                    console.error("Copy failed:", err);
                });
        });
    }
});

document.getElementById("uploadBtn").addEventListener("click", function () {
    document.getElementById("uploadInput").click();
});

document.getElementById("uploadInput").addEventListener("change", function (e) {
    const files = e.target.files;
    const container = document.getElementById("add_images");

    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        const reader = new FileReader();
        reader.onload = function (event) {
            const wrapper = document.createElement("div");
            wrapper.className = "preview_image position-relative";
            wrapper.style.width = "48%";

            // Create a new file input element
            const fileInput = document.createElement("input");
            fileInput.type = "file";
            fileInput.name = "preview_images";
            fileInput.className = "d-none file-input";
            fileInput.accept = "image/*";

            // Set its value with the uploaded file using DataTransfer
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;

            // Append all elements to wrapper
            wrapper.innerHTML = `
                <img src="${event.target.result}"
                     alt="preview"
                     class="rounded w-100 preview_images border" />

                <div class="action-buttons d-flex flex-column gap-2 position-absolute top-0 end-0 m-1 z-index-1 p-1 rounded">
                    <button type="button"
                            class="btn btn-action btn-delete bg-danger text-light"
                            title="Remove">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;

            // Append the file input into the wrapper
            wrapper.appendChild(fileInput);

            // Delete functionality
            wrapper.querySelector(".btn-delete").addEventListener("click", function () {
                wrapper.remove();
            });

            container.appendChild(wrapper);
        };

        reader.readAsDataURL(file);
    }

    // Reset input for future uploads
    e.target.value = "";
});
