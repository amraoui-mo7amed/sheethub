class ImageUploader {
    constructor(element) {
        this.wrapper = element;
        this.input = element.querySelector('input[type="file"]');
        this.preview = element.querySelector('.upload-preview');
        this.uploadId = element.dataset.uploadId;

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File input change
        this.input.addEventListener('change', (e) => this.handleFileSelect(e));

        // Drag and drop
        this.wrapper.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.wrapper.classList.add('dragover');
        });

        this.wrapper.addEventListener('dragleave', () => {
            this.wrapper.classList.remove('dragover');
        });

        this.wrapper.addEventListener('drop', (e) => {
            e.preventDefault();
            this.wrapper.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                this.input.files = e.dataTransfer.files;
                this.handleFileSelect({ target: this.input });
            }
        });

        // Remove image button
        const removeBtn = this.wrapper.querySelector('.remove-image');
        if (removeBtn) {
            removeBtn.addEventListener('click', () => this.removeImage());
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        
        if (!file) return;

        // Validate file type
        if (!file.type.startsWith('image/')) {
            this.showError('Please select an image file');
            return;
        }

        // Validate file size (5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showError('File size should not exceed 5MB');
            return;
        }

        const reader = new FileReader();
        
        reader.onload = (e) => {
            this.updatePreview(e.target.result);
        };

        reader.readAsDataURL(file);
    }

    updatePreview(imageUrl) {
        const template = `
            <img src="${imageUrl}" alt="Preview" class="preview-image">
        `;

        this.preview.innerHTML = template;
        this.preview.classList.add('has-image');

    }

    removeImage() {
        this.input.value = '';
        const placeholder = `
            <div class="upload-placeholder">
                <i class="fas fa-cloud-upload-alt"></i>
                <p>Drop your image here or click to browse</p>
                <span class="upload-size">Maximum file size: 5MB</span>
            </div>
        `;
        
        this.preview.innerHTML = placeholder;
        this.preview.classList.remove('has-image');
    }

    showError(message) {
        const error = document.createElement('div');
        error.className = 'upload-error';
        error.textContent = message;

        // Remove existing error if any
        const existingError = this.wrapper.querySelector('.upload-error');
        if (existingError) {
            existingError.remove();
        }

        this.wrapper.appendChild(error);
        setTimeout(() => error.remove(), 3000);
    }
}

// Initialize all image uploaders on page load
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.image-upload-wrapper').forEach(wrapper => {
        new ImageUploader(wrapper);
    });
});