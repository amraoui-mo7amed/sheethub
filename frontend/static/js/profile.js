document.addEventListener('DOMContentLoaded', function() {
    // Handle ticket button selection
    const ticketButtons = document.querySelectorAll('.ticket-btn');
    const ticketInputs = document.querySelectorAll('.ticket-input');

    // Get event plan radio buttons
    const freeRadio = document.getElementById('free');
    const paidRadio = document.getElementById('paid');
    const ticketsDetails = document.getElementById('ticketsDetails');

    // Function to toggle ticket fields based on event plan
    function togglePaidEventFields() {
        if (paidRadio && freeRadio && ticketsDetails) {
            const isPaid = paidRadio.checked;
            ticketsDetails.style.display = isPaid ? 'block' : 'none';
            
            // Enable/disable all ticket inputs
            ticketButtons.forEach(button => {
                const ticketType = button.dataset.ticketType;
                const seatsInput = document.getElementById(`${ticketType}_seats`);
                const priceInput = document.getElementById(`${ticketType}_price`);
                
                if (isPaid) {
                    // For paid events, allow ticket selection
                    button.disabled = false;
                    if (button.classList.contains('active')) {
                        seatsInput.disabled = false;
                        priceInput.disabled = false;
                    }
                } else {
                    // For free events, disable all ticket fields
                    button.disabled = true;
                    button.classList.remove('active');
                    seatsInput.disabled = true;
                    priceInput.disabled = true;
                    seatsInput.value = '';
                    priceInput.value = '';
                }
            });
        }
    }

    // Initialize based on current state
    togglePaidEventFields();

    // Add event listeners for radio buttons
    if (freeRadio) {
        freeRadio.addEventListener('change', togglePaidEventFields);
    }
    if (paidRadio) {
        paidRadio.addEventListener('change', togglePaidEventFields);
    }

    // Handle ticket button selection
    ticketButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Toggle button selection
            this.classList.toggle('active');
            
            // Enable/disable inputs based on selection
            const ticketType = this.dataset.ticketType;
            const seatsInput = document.getElementById(`${ticketType}_seats`);
            const priceInput = document.getElementById(`${ticketType}_price`);
            
            if (this.classList.contains('active')) {
                // Enable inputs and set default values if not set
                seatsInput.disabled = false;
                priceInput.disabled = false;
                if (!seatsInput.value) seatsInput.value = '0';
                if (!priceInput.value) priceInput.value = '0.00';
            } else {
                // Disable inputs
                seatsInput.disabled = true;
                priceInput.disabled = true;
                seatsInput.value = '';
                priceInput.value = '';
            }
        });
    });

    // Initialize inputs based on button state
    ticketButtons.forEach(button => {
        const ticketType = button.dataset.ticketType;
        const seatsInput = document.getElementById(`${ticketType}_seats`);
        const priceInput = document.getElementById(`${ticketType}_price`);
        
        if (button.classList.contains('active')) {
            seatsInput.disabled = false;
            priceInput.disabled = false;
        } else {
            seatsInput.disabled = true;
            priceInput.disabled = true;
        }
    });
});
