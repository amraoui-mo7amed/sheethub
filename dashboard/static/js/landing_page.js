document.addEventListener('DOMContentLoaded', function () {
    // Quantity input buttons functionality
    const quantityInput = document.getElementById('quantity');
    const minusBtn = quantityInput.parentElement.querySelector('.minus');
    const plusBtn = quantityInput.parentElement.querySelector('.plus');

    // Decrease quantity
    minusBtn.addEventListener('click', function () {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > parseInt(quantityInput.min)) {
            quantityInput.value = currentValue - 1;
            quantityInput.dispatchEvent(new Event('change'));
        }
    });

    // Increase quantity
    plusBtn.addEventListener('click', function () {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
        quantityInput.dispatchEvent(new Event('change'));
    });

    // Phone number validation
    const phoneInput = document.getElementById('phone');
    const form = phoneInput.closest('form');

    // Client-side validation
    form.addEventListener('submit', function (e) {
        const phoneValue = phoneInput.value.trim();
        const phoneRegex = /^[567]\d{8}$/;

        if (!phoneRegex.test(phoneValue)) {
            e.preventDefault();
            alert(
                '{% if lang == "ar" %}' +
                'الرجاء إدخال رقم هاتف صحيح. يجب أن يبدأ بـ 5، 6 أو 7 ويحتوي على 9 أرقام' +
                '{% elif lang == "fr" %}' +
                'Veuillez entrer un numéro de téléphone valide. Doit commencer par 5, 6 ou 7 et contenir 9 chiffres' +
                '{% else %}' +
                'Please enter a valid phone number. Must start with 5, 6, or 7 and be 9 digits' +
                '{% endif %}'
            );
            phoneInput.focus();
            return false;
        }
        return true;
    });

    // Auto-format and validate on input
    phoneInput.addEventListener('input', function (e) {
        // Remove any non-digit characters
        let value = e.target.value.replace(/\D/g, '');

        // Limit to 9 digits
        if (value.length > 9) {
            value = value.slice(0, 9);
        }

        // Update the input value
        e.target.value = value;

        // Validate first digit
        if (value.length > 0 && !['5', '6', '7'].includes(value[0])) {
            e.target.setCustomValidity(
                '{% if lang == "ar" %}' +
                'يجب أن يبدأ رقم الهاتف بـ 5، 6 أو 7' +
                '{% elif lang == "fr" %}' +
                'Le numéro doit commencer par 5, 6 ou 7' +
                '{% else %}' +
                'Phone number must start with 5, 6, or 7' +
                '{% endif %}'
            );
        } else if (value.length > 0 && value.length < 9) {
            e.target.setCustomValidity(
                '{% if lang == "ar" %}' +
                'يجب أن يتكون رقم الهاتف من 9 أرقام' +
                '{% elif lang == "fr" %}' +
                'Le numéro doit contenir 9 chiffres' +
                '{% else %}' +
                'Phone number must be 9 digits' +
                '{% endif %}'
            );
        } else {
            e.target.setCustomValidity('');
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const wilayaSelect = document.querySelector("#wilaya");
    const communeSelect = document.querySelector("#commune");
    const langCode = document.documentElement.lang || "ar"; // Default to 'ar' if not found
    console.log(langCode);
    
    if (!wilayaSelect || !communeSelect) return;

    const wilayaInput = wilayaSelect.querySelector("input[type='hidden']");
    const communeInput = communeSelect.querySelector("input[type='hidden']");
    const communeOptionsContainer = communeSelect.querySelector(".select-options");
    const communeSelectedSpan = communeSelect.querySelector(".selected-value");

    function populateCommunes(communes) {
        // Reset options with search box
        communeOptionsContainer.innerHTML = `
            <div class="search-box">
                <input type="text" placeholder="إبحث" class="select-search" />
            </div>
        `;

        communes.forEach(commune => {
            const option = document.createElement("div");
            option.classList.add("select-option");
            option.setAttribute("data-value", commune.commune_name);
            option.textContent = commune.commune_name;
            communeOptionsContainer.appendChild(option);

            option.addEventListener("click", function () {
                communeInput.value = this.dataset.value;
                if (communeSelectedSpan) communeSelectedSpan.textContent = this.textContent;
            });
        });

        // Auto-select previous value or first commune
        const current = communeInput.value;
        const found = communes.find(c => c.commune_name === current);
        const defaultCommune = found ? found.commune_name : communes[0]?.commune_name;

        if (defaultCommune) {
            communeInput.value = defaultCommune;
            if (communeSelectedSpan) communeSelectedSpan.textContent = defaultCommune;
        }
    }

    // Load communes on wilaya select
    wilayaSelect.querySelectorAll(".select-option").forEach(option => {
        option.addEventListener("click", function () {
            const selectedWilayaCode = this.dataset.value;
            wilayaInput.value = selectedWilayaCode;

            fetch(`/get-communes/${selectedWilayaCode}/${langCode}/`)
                .then(response => response.json())
                .then(data => populateCommunes(data))
                .catch(error => console.error("Failed to fetch communes:", error));
        });
    });

    // Auto-load communes if wilaya is pre-selected
    const preselectedWilaya = wilayaInput.value;
    if (preselectedWilaya) {
        fetch(`/get-communes/${preselectedWilaya}/${langCode}/`)
            .then(response => response.json())
            .then(data => populateCommunes(data))
            .catch(error => console.error("Failed to preload communes:", error));
    }
});


document.addEventListener("DOMContentLoaded", function () {
    // Animate on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.image-animate').forEach(el => observer.observe(el));

    // Zoomable gallery
    const previewImages = Array.from(document.querySelectorAll('.zoomable-image'));
    let currentIndex = -1;

    function createOverlay(img) {
        const overlay = document.createElement("div");
        overlay.className = "image-overlay";

        const closeBtn = document.createElement("span");
        closeBtn.className = "image-overlay-close";
        closeBtn.innerHTML = "&times;";
        closeBtn.onclick = closeOverlay;

        const imgElement = document.createElement("img");
        imgElement.src = img.src;
        imgElement.alt = img.alt || "";

        const prevBtn = document.createElement("div");
        prevBtn.className = "image-overlay-nav image-overlay-prev";
        prevBtn.innerHTML = "&#10094;";
        prevBtn.onclick = () => showImage(currentIndex - 1);

        const nextBtn = document.createElement("div");
        nextBtn.className = "image-overlay-nav image-overlay-next";
        nextBtn.innerHTML = "&#10095;";
        nextBtn.onclick = () => showImage(currentIndex + 1);

        overlay.appendChild(closeBtn);
        overlay.appendChild(prevBtn);
        overlay.appendChild(nextBtn);
        overlay.appendChild(imgElement);

        document.body.appendChild(overlay);

        // Animate after slight delay
        requestAnimationFrame(() => overlay.classList.add("loaded"));

        // ESC / arrow keys
        function keyHandler(e) {
            if (e.key === "Escape") closeOverlay();
            else if (e.key === "ArrowLeft") showImage(currentIndex - 1);
            else if (e.key === "ArrowRight") showImage(currentIndex + 1);
        }

        document.addEventListener("keydown", keyHandler);
        overlay._keyHandler = keyHandler;

        // Swipe support
        let startX = null;
        overlay.addEventListener("touchstart", (e) => {
            startX = e.touches[0].clientX;
        });
        overlay.addEventListener("touchend", (e) => {
            if (!startX) return;
            const endX = e.changedTouches[0].clientX;
            const diff = startX - endX;
            if (Math.abs(diff) > 40) {
                diff > 0 ? showImage(currentIndex + 1) : showImage(currentIndex - 1);
            }
            startX = null;
        });

        return overlay;
    }

    let overlayRef = null;

    function showImage(index) {
        if (index < 0 || index >= previewImages.length) return;

        currentIndex = index;
        const newImg = previewImages[currentIndex];

        if (overlayRef) {
            const imgEl = overlayRef.querySelector("img");
            imgEl.src = newImg.src;
            imgEl.alt = newImg.alt || "";
        } else {
            overlayRef = createOverlay(newImg);
        }
    }

    function closeOverlay() {
        if (overlayRef) {
            document.removeEventListener("keydown", overlayRef._keyHandler);
            overlayRef.remove();
            overlayRef = null;
            currentIndex = -1;
        }
    }

    previewImages.forEach((img, index) => {
        img.addEventListener("click", () => showImage(index));
    });
});
