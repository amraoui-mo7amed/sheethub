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