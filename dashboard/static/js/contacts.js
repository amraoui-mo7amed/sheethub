document.addEventListener('DOMContentLoaded', () => {
    const mailModal = document.getElementById('mailModal');
    mailModal.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget; // clicked button
        const email = button.getAttribute('data-email');
        const name = button.getAttribute('data-name');
        const pk = button.getAttribute('data-pk');

        mailModal.querySelector('#mailTo').value = email;
        mailModal.querySelector('#contactPk').value = pk;
        mailModal.querySelector('.contact-name').textContent = `${name}`;
    });
});