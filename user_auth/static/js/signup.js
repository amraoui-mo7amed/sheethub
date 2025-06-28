document.addEventListener('DOMContentLoaded', function() {
    // Password toggle functionality
    document.querySelectorAll('.password-toggle').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const type = passwordInput.getAttribute('type');
            const newType = type === 'password' ? 'text' : 'password';
            const newIcon = type === 'password' ? 'fa-eye-slash' : 'fa-eye';

            passwordInput.setAttribute('type', newType);
            this.querySelector('i').classList.remove('fa-eye', 'fa-eye-slash');
            this.querySelector('i').classList.add(newIcon);
        });
    });

    // Password match validation
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const form = document.querySelector('form');

    form.addEventListener('submit', function(e) {
        if (password1.value !== password2.value) {
            e.preventDefault();
            alert(gettext('Passwords do not match'));
        }
    });

    // Date of birth validation
    const dateInput = document.querySelector('input[name="date_of_birth"]');
    if (dateInput) {
        const today = new Date();
        const minDate = new Date();
        minDate.setFullYear(today.getFullYear() - 100); // Max age 100
        const maxDate = new Date();
        maxDate.setFullYear(today.getFullYear() - 13); // Min age 13

        dateInput.setAttribute('min', minDate.toISOString().split('T')[0]);
        dateInput.setAttribute('max', maxDate.toISOString().split('T')[0]);

        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            if (selectedDate > maxDate) {
                alert(gettext('You must be at least 13 years old to register'));
                this.value = '';
            }
        });
    }

    // Mobile number validation
    const mobileInput = document.querySelector('input[name="mobile"]');
    if (mobileInput) {
        mobileInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 9) {
                this.value = this.value.slice(0, 9);
            }
        });
    }

    // Custom dropdown functionality
    const dropdowns = document.querySelectorAll('.custom-dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        const items = dropdown.querySelectorAll('.dropdown-item');
        const hiddenInput = dropdown.querySelector('input[type="hidden"]');
        const selectedText = toggle.querySelector('.selected-text');

        // Toggle dropdown
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('show');
            toggle.classList.toggle('active');
        });

        // Select item
        items.forEach(item => {
            item.addEventListener('click', () => {
                const value = item.dataset.value;
                const text = item.textContent;
                
                // Update hidden input
                hiddenInput.value = value;
                
                // Update toggle text
                selectedText.textContent = text;
                
                // Update selected state
                items.forEach(i => i.classList.remove('selected'));
                item.classList.add('selected');
                
                // Close dropdown
                menu.classList.remove('show');
                toggle.classList.remove('active');
                
                // Trigger change event
                hiddenInput.dispatchEvent(new Event('change'));
            });
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            menu.classList.remove('show');
            toggle.classList.remove('active');
        });
    });
});