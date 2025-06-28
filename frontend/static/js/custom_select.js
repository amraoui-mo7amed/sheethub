document.addEventListener('DOMContentLoaded', function () {
    // Initialize all custom selects on the page
    document.querySelectorAll('.custom-select').forEach(select => {
        const header = select.querySelector('.select-header');
        const options = select.querySelector('.select-options');
        const hiddenInput = select.querySelector('input[type="hidden"]');
        const selectedValue = select.querySelector('.selected-value');
        const searchInput = select.querySelector('.select-search');
        const arrow = select.querySelector('.arrow');

        // Initialize selected state
        function initializeSelect() {
            // Check if there's a selected value
            const selectedOption = select.querySelector('.select-option.selected');
            if (selectedOption) {
                selectedValue.textContent = selectedOption.textContent;
                hiddenInput.value = selectedOption.dataset.value;
            } else {
                // No option selected, show default label
                hiddenInput.value = '';
            }
        }

        // Initialize on load
        initializeSelect();

        // Handle option selection
        select.querySelectorAll('.select-option').forEach(option => {
            option.addEventListener('click', function () {
                // Update selected value display
                selectedValue.textContent = this.textContent;
                
                // Update hidden input value
                hiddenInput.value = this.dataset.value;

                // Update selected state
                select.querySelectorAll('.select-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                this.classList.add('selected');

                // Close dropdown
                options.classList.remove('show');
                arrow.classList.remove('rotate');

                // Trigger change event
                hiddenInput.dispatchEvent(new Event('change'));
            });
        });

        // Reset to default when no option is selected
        hiddenInput.addEventListener('change', function() {
            if (!this.value) {
                selectedValue.textContent = defaultLabel;
                select.querySelectorAll('.select-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
            }
        });

        // Toggle dropdown visibility
        header.addEventListener('click', function (e) {
            e.stopPropagation();
            options.classList.toggle('show');
            arrow.classList.toggle('rotate');

            // Scroll to selected option when opening
            if (options.classList.contains('show')) {
                const selectedOption = select.querySelector('.select-option.selected');
                if (selectedOption) {
                    selectedOption.scrollIntoView({ block: 'nearest' });
                }
            }
        });

        // Handle option selection
        select.querySelectorAll('.select-option').forEach(option => {
            option.addEventListener('click', function () {
                // Update selected value display
                selectedValue.textContent = this.textContent;

                // Update hidden input value
                hiddenInput.value = this.dataset.value;

                // Update selected state
                select.querySelectorAll('.select-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                this.classList.add('selected');

                // Close dropdown
                options.classList.remove('show');
                arrow.classList.remove('rotate');

                // Trigger change event
                hiddenInput.dispatchEvent(new Event('change'));
            });
        });

        // Filter options based on search input
        if (searchInput) {
            searchInput.addEventListener('input', function () {
                const searchTerm = this.value.toLowerCase();
                select.querySelectorAll('.select-option').forEach(option => {
                    const text = option.textContent.toLowerCase();
                    option.style.display = text.includes(searchTerm) ? 'block' : 'none';
                });
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function () {
        document.querySelectorAll('.select-options').forEach(options => {
            options.classList.remove('show');
        });
        document.querySelectorAll('.arrow').forEach(arrow => {
            arrow.classList.remove('rotate');
        });
    });

    // Prevent dropdown from closing when clicking inside
    document.querySelectorAll('.select-options').forEach(options => {
        options.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    });
});