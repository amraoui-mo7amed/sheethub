document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');
    const form = document.getElementById('smtpConfigForm');
    
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }

    // Test Connection button handler
    const testConnectionBtn = document.getElementById('testConnection');
    if (testConnectionBtn) {
        testConnectionBtn.addEventListener('click', async function() {
            if (!form) return;
            
            const originalBtnText = testConnectionBtn.innerHTML;
            const resultDiv = document.getElementById('text_result') || createResultDiv(form);
            
            try {
                // Show loading state
                testConnectionBtn.disabled = true;
                testConnectionBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Testing...';
                
                const formData = new FormData(form);
                const response = await fetch(testConnectionBtn.getAttribute('data-test-url'), {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    credentials: 'same-origin'
                });

                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    if (data.success) {
                        showResult('success', 'Connection test successful!', resultDiv);
                    } else {
                        showResult('danger', data.error || 'Connection test failed', resultDiv);
                    }
                } else {
                    const text = await response.text();
                    console.error('Non-JSON response:', text);
                    showResult('danger', 'Unexpected response from server. Please check the console for details.', resultDiv);
                }
            } catch (error) {
                console.error('Error:', error);
                showResult('danger', 'Error testing connection', resultDiv);
            } finally {
                testConnectionBtn.disabled = false;
                testConnectionBtn.innerHTML = originalBtnText;
            }
        });
    }

    // Create result div if it doesn't exist
    function createResultDiv(formElement) {
        let resultDiv = document.getElementById('test_result');
        return resultDiv;
    }

    // Show result message with Bootstrap styling
    function showResult(type, message, container) {
        if (!container) return;
        
        container.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }
});