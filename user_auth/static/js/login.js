document.addEventListener('DOMContentLoaded', function() {
    const passwordToggle = document.querySelector('.password-toggle');
    const passwordInput = document.querySelector('#password');

    passwordToggle.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type');
        const newType = type === 'password' ? 'text' : 'password';
        const newIcon = type === 'password' ? 'fa-eye-slash' : 'fa-eye';

        passwordInput.setAttribute('type', newType);
        passwordToggle.querySelector('i').classList.remove('fa-eye', 'fa-eye-slash');
        passwordToggle.querySelector('i').classList.add(newIcon);
    });
});