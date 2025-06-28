document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const freeRadio = document.getElementById('free');
    const paidRadio = document.getElementById('paid');
    const ticketsDetails = document.getElementById('ticketsDetails');
    const ticketButtons = document.querySelectorAll('.ticket-btn');

    // Function to handle ticket button selection
    function handleTicketSelection(button) {
        // Toggle active class on clicked button
        button.classList.toggle('active');
        
        // Enable/disable inputs based on selection
        const ticketType = button.dataset.ticketType;
        const seatsInput = document.getElementById(`${ticketType}_seats`);
        const priceInput = document.getElementById(`${ticketType}_price`);
        
        if (button.classList.contains('active')) {
            seatsInput.disabled = false;
            priceInput.disabled = false;
            if (!seatsInput.value) seatsInput.value = '0';
            if (!priceInput.value) priceInput.value = '0.00';
        } else {
            seatsInput.disabled = true;
            priceInput.disabled = true;
            seatsInput.value = '';
            priceInput.value = '';
        }
    }

    // Function to toggle ticket section visibility
    function toggleTicketSection() {
        if (paidRadio && freeRadio && ticketsDetails) {
            const isPaid = paidRadio.checked;
            ticketsDetails.style.display = isPaid ? 'block' : 'none';
            
            // Reset all ticket buttons and inputs when switching to free
            if (!isPaid) {
                ticketButtons.forEach(button => {
                    button.classList.remove('active');
                    const ticketType = button.dataset.ticketType;
                    const seatsInput = document.getElementById(`${ticketType}_seats`);
                    const priceInput = document.getElementById(`${ticketType}_price`);
                    seatsInput.value = '';
                    priceInput.value = '';
                    seatsInput.disabled = true;
                    priceInput.disabled = true;
                });
            }
        }
    }

    // Initialize based on current state
    toggleTicketSection();

    // Add event listeners for ticket buttons
    ticketButtons.forEach(button => {
        button.addEventListener('click', function() {
            handleTicketSelection(this);
        });
    });

    // Add event listeners for radio buttons
    if (freeRadio) {
        freeRadio.addEventListener('change', toggleTicketSection);
    }
    if (paidRadio) {
        paidRadio.addEventListener('change', toggleTicketSection);
    }
});