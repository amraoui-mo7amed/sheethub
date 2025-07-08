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
        pixelAsterisk.style.display = pixelToggle.checked ? "inline" : "none";
    }

    function toggleAdditionalImages() {
        additionalAsterisk.style.display = additionalToggle.checked ? "inline" : "none";
    }

    pixelToggle.addEventListener("change", togglePixelField);
    additionalToggle.addEventListener("change", toggleAdditionalImages);

    togglePixelField();
    toggleAdditionalImages();
});
