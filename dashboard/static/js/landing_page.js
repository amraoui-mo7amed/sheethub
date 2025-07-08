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

            fetch(`/get-communes/${selectedWilayaCode}/`)
                .then(response => response.json())
                .then(data => populateCommunes(data))
                .catch(error => console.error("Failed to fetch communes:", error));
        });
    });

    // Auto-load communes if wilaya is pre-selected
    const preselectedWilaya = wilayaInput.value;
    if (preselectedWilaya) {
        fetch(`/get-communes/${preselectedWilaya}/`)
            .then(response => response.json())
            .then(data => populateCommunes(data))
            .catch(error => console.error("Failed to preload communes:", error));
    }
});
