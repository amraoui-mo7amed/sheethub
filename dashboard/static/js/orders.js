// static/js/orders.js

document.addEventListener('DOMContentLoaded', function () {
    // --- START: Global Elements (Used by both Search and Filter) ---
    const tableBody = document.querySelector('table tbody'); // The tbody where order rows are
    const allTableRows = tableBody ? Array.from(tableBody.querySelectorAll('tr')) : []; // Get all rows once

    // --- Helper for combined search and filter logic ---
    function applyCombinedFiltersAndSearch() {
        const searchQuery = searchInput.value.toLowerCase().trim();
        const selectedStatus = filterStatusSelect.value.toLowerCase();

        if (!tableBody) {
            console.warn("Table tbody not found. Cannot apply filters or search.");
            return;
        }

        allTableRows.forEach(row => {
            const rowStatus = row.dataset.status; // Get status from data-attribute
            let matchesFilter = true;
            let matchesSearch = true;

            // Apply Search Query (if it passed the filter)
            if (searchQuery !== '') {
                let rowContainsQuery = false;
                const cells = row.querySelectorAll('th, td'); // Check all cells for search query
                for (const cell of cells) {
                    if (cell.textContent.toLowerCase().includes(searchQuery)) {
                        rowContainsQuery = true;
                        break; // Found a match in this row, no need to check other cells
                    }
                }
                if (!rowContainsQuery) {
                    matchesSearch = false;
                }
            }

            // Decide whether to show or hide the row
            if (matchesFilter && matchesSearch) {
                row.style.display = ''; // Show the row
                // Add highlight only if there's an active search query
                if (searchQuery !== '') {
                    row.classList.add('highlight-row');
                } else {
                    row.classList.remove('highlight-row');
                }
            } else {
                row.style.display = 'none'; // Hide the row
                row.classList.remove('highlight-row'); // Remove highlight if hidden
            }
        });
    }
    // --- END: Global Elements & Helper ---


    // --- START: Search Widget related code ---
    const searchButton = document.getElementById('searchOrders');
    const floatingSearchWidget = document.getElementById('floatingSearchWidget');
    const closeSearchBtn = document.getElementById('closeSearchBtn');
    const searchInput = document.getElementById('searchInput');

    // Create a semi-transparent overlay dynamically for the search widget
    const searchOverlay = document.createElement('div');
    searchOverlay.id = 'floatingSearchOverlay';
    searchOverlay.classList.add('floating-search-overlay');
    document.body.appendChild(searchOverlay);

    // --- Helper Functions for Search Widget UI ---
    function showSearchWidget() {
        floatingSearchWidget.classList.add('show');
        searchOverlay.classList.add('show');
        searchInput.focus(); // Automatically focus on the search input
        hideFilterWidget(); // Hide filter widget if search opens
    }

    function hideSearchWidget() {
        floatingSearchWidget.classList.remove('show');
        searchOverlay.classList.remove('show');
    }

    // --- Event Listeners for Search Widget ---
    if (searchButton) {
        searchButton.addEventListener('click', function () {
            if (floatingSearchWidget.classList.contains('show')) {
                hideSearchWidget();
            } else {
                showSearchWidget();
                applyCombinedFiltersAndSearch(); // Apply current filters/search on show
            }
        });
    }

    if (closeSearchBtn) {
        closeSearchBtn.addEventListener('click', function () {
            searchInput.value = ''; // Clear input on close
            hideSearchWidget();
            applyCombinedFiltersAndSearch(); // Re-apply filters with cleared search
        });
    }

    if (searchOverlay) {
        searchOverlay.addEventListener('click', function (event) {
            if (event.target === searchOverlay) {
                hideSearchWidget();
            }
        });
    }

    // Live search as user types
    if (searchInput) {
        searchInput.addEventListener('input', applyCombinedFiltersAndSearch);

        // Prevent default form submission on Enter key press in the search input (if it were in a form)
        searchInput.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
            }
        });
    }
    // --- END: Search Widget related code ---


    // --- START: Filter Widget related code ---
    const filterOrdersBtn = document.getElementById('filterOrdersBtn');
    const floatingFilterWidget = document.getElementById('floatingFilterWidget');
    const closeFilterBtn = document.getElementById('closeFilterBtn');
    const filterStatusSelect = document.getElementById('filterStatusSelect'); // The custom select element
    const applyFilterBtn = document.getElementById('applyFilterBtn'); // The apply button

    // Create a semi-transparent overlay dynamically for the filter widget
    const filterOverlay = document.createElement('div');
    filterOverlay.id = 'floatingFilterOverlay';
    filterOverlay.classList.add('floating-filter-overlay');
    document.body.appendChild(filterOverlay);

    // --- Helper Functions for Filter Widget UI ---
    function showFilterWidget() {
        floatingFilterWidget.classList.add('show');
        filterOverlay.classList.add('show');
        hideSearchWidget(); // Hide search widget if filter opens
    }

    function hideFilterWidget() {
        floatingFilterWidget.classList.remove('show');
        filterOverlay.classList.remove('show');
    }

    // --- Event Listeners for Filter Widget ---
    if (filterOrdersBtn) {
        filterOrdersBtn.addEventListener('click', function () {
            if (floatingFilterWidget.classList.contains('show')) {
                hideFilterWidget();
            } else {
                showFilterWidget();
                applyCombinedFiltersAndSearch(); // Apply current filters/search on show
            }
        });
    }

    if (closeFilterBtn) {
        closeFilterBtn.addEventListener('click', function () {
            // Option 1: Clear the filter select on close
            // filterStatusSelect.value = '';
            hideFilterWidget();
            applyCombinedFiltersAndSearch(); // Re-apply search with current filter (or cleared filter)
        });
    }

    if (filterOverlay) {
        filterOverlay.addEventListener('click', function (event) {
            if (event.target === filterOverlay) {
                hideFilterWidget();
            }
        });
    }

    // Apply filters when the "Apply Filters" button is clicked
    if (applyFilterBtn) {
        applyFilterBtn.addEventListener('click', function () {
            applyCombinedFiltersAndSearch();
            hideFilterWidget(); // Optionally hide widget after applying
        });
    }

    // Or apply filters instantly when the select value changes
    if (filterStatusSelect) {
        filterStatusSelect.addEventListener('change', applyCombinedFiltersAndSearch);
    }
    // --- END: Filter Widget related code ---


    // --- START: Global Escape Key Listener (for both widgets) ---
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            if (floatingSearchWidget.classList.contains('show')) {
                searchInput.value = ''; // Clear search input
                hideSearchWidget();
                applyCombinedFiltersAndSearch(); // Re-apply without search
            }
            if (floatingFilterWidget.classList.contains('show')) {
                // filterStatusSelect.value = ''; // Optionally clear filter selection
                hideFilterWidget();
                applyCombinedFiltersAndSearch(); // Re-apply without filter (or with current filter)
            }
        }
    });
    // --- END: Global Escape Key Listener ---


    // --- START: Order Details Modal related code (Remains the same as before) ---
    const orderDetailsModal = document.getElementById('orderDetailsModal');
    if (!orderDetailsModal) {
        console.warn("Order Details Modal not found. Order modal functionality disabled.");
        return;
    }

    const modalOrderId = document.getElementById('modalOrderId');
    const modalOrderFullName = document.getElementById('modalOrderFullName');
    const modalOrderPhoneNumber = document.getElementById('modalOrderPhoneNumber');
    const modalOrderWilaya = document.getElementById('modalOrderWilaya');
    const modalOrderCommune = document.getElementById('modalOrderCommune');
    const modalProductName = document.getElementById('modalProductName');
    const modalProductPrice = document.getElementById('modalProductPrice');
    const modalOrderQuantity = document.getElementById('modalOrderQuantity');
    const modalOrderTotalPrice = document.getElementById('modalOrderTotalPrice');
    const modalOrderCreatedAt = document.getElementById('modalOrderCreatedAt');

    const modalLoadingSpinner = document.getElementById('modalLoadingSpinner');
    const modalError = document.getElementById('modalError');
    const modalContent = document.getElementById('modalContent');

    const dropdownOrderStatus = document.getElementById('dropdownOrderStatus');
    const modalOrderStatusText = document.getElementById('modalOrderStatusText');
    const modalStatusDropdownMenu = document.getElementById('modalStatusDropdownMenu');
    const statusUpdatingSpinner = document.getElementById('statusUpdatingSpinner');

    const STATUS_OPTIONS = [
        { value: 'pending', display: 'Pending', badgeClass: 'bg-warning text-dark' },
        { value: 'confirmed', display: 'Confirmed', badgeClass: 'bg-info text-light' },
        { value: 'shipped', display: 'Shipped', badgeClass: 'bg-primary text-light' },
        { value: 'delivered', display: 'Delivered', badgeClass: 'bg-success text-light' },
        { value: 'cancelled', display: 'Cancelled', badgeClass: 'bg-danger text-light' },
    ];

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateOrderStatusUI(statusValueFromBackend) {
        const normalizedStatusValue = statusValueFromBackend.toLowerCase();
        const statusOption = STATUS_OPTIONS.find(option => option.value === normalizedStatusValue);

        if (statusOption && dropdownOrderStatus && modalOrderStatusText) {
            modalOrderStatusText.textContent = statusOption.display;

            dropdownOrderStatus.classList.remove(
                'bg-warning', 'bg-info', 'bg-primary', 'bg-success', 'bg-danger', 'bg-secondary',
                'text-dark', 'text-light'
            );
            dropdownOrderStatus.classList.add(...statusOption.badgeClass.split(' '));

            modalStatusDropdownMenu.querySelectorAll('.dropdown-item').forEach(item => {
                item.classList.remove('active');
                item.removeAttribute('aria-current');
                item.classList.remove('disabled');
                item.removeAttribute('tabindex');

                if (item.dataset.statusValue === normalizedStatusValue) {
                    item.classList.add('active');
                    item.setAttribute('aria-current', 'true');
                    item.classList.add('disabled');
                    item.setAttribute('tabindex', '-1');
                }
            });
        }
    }

    orderDetailsModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const orderDetailsUrl = button.dataset.orderDetailsUrl;
        const updateStatusUrl = orderDetailsModal.dataset.updateStatusUrl;

        let currentOrderData = null;

        modalError.style.display = 'none';
        modalContent.style.display = 'none';
        statusUpdatingSpinner.style.display = 'none';
        dropdownOrderStatus.disabled = true;
        modalLoadingSpinner.style.display = 'block';

        fetch(orderDetailsUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    currentOrderData = data.order;

                    modalOrderId.textContent = String(currentOrderData.id).padStart(4, '0');
                    modalOrderFullName.textContent = currentOrderData.full_name;
                    modalOrderPhoneNumber.textContent = currentOrderData.phone_number;
                    modalOrderWilaya.textContent = currentOrderData.wilaya;
                    modalOrderCommune.textContent = currentOrderData.commune;
                    modalProductName.textContent = currentOrderData.product.name;
                    modalProductPrice.textContent = parseFloat(currentOrderData.product.price).toFixed(2);
                    modalOrderQuantity.textContent = currentOrderData.quantity;
                    modalOrderTotalPrice.textContent = parseFloat(currentOrderData.total_price).toFixed(2);

                    const createdAtDate = new Date(currentOrderData.created_at);
                    modalOrderCreatedAt.textContent = createdAtDate.toLocaleString('en-US', {
                        year: 'numeric', month: 'short', day: 'numeric',
                        hour: '2-digit', minute: '2-digit', hour12: true
                    });

                    updateOrderStatusUI(currentOrderData.status);

                    modalStatusDropdownMenu.innerHTML = '';
                    const currentNormalizedStatus = currentOrderData.status.toLowerCase();

                    STATUS_OPTIONS.forEach(option => {
                        const listItem = document.createElement('li');
                        const link = document.createElement('a');
                        link.classList.add('dropdown-item');
                        link.href = '#';
                        link.textContent = option.display;
                        link.dataset.statusValue = option.value;
                        link.dataset.orderId = currentOrderData.id;

                        if (option.value === currentNormalizedStatus) {
                            link.classList.add('active', 'disabled');
                            link.setAttribute('aria-current', 'true');
                            link.setAttribute('tabindex', '-1');
                        }
                        listItem.appendChild(link);
                        modalStatusDropdownMenu.appendChild(listItem);
                    });

                    modalLoadingSpinner.style.display = 'none';
                    modalContent.style.display = 'block';
                    dropdownOrderStatus.disabled = false;

                } else {
                    modalLoadingSpinner.style.display = 'none';
                    modalError.textContent = data.message || 'Failed to load order details due to a server error.';
                    modalError.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error fetching order details:', error);
                modalLoadingSpinner.style.display = 'none';
                modalError.style.display = 'block';
                modalError.textContent = 'Network error or invalid response. Please check your connection.';
            });
    });

    modalStatusDropdownMenu.addEventListener('click', function (e) {
        e.preventDefault();
        const target = e.target;

        if (target.classList.contains('dropdown-item') && !target.classList.contains('disabled')) {
            const newStatus = target.dataset.statusValue;
            const orderId = target.dataset.orderId;
            const updateStatusUrl = orderDetailsModal.dataset.updateStatusUrl;

            if (!orderId || !newStatus || !updateStatusUrl) {
                console.error('Missing order ID, new status, or update URL for status update.');
                Swal.fire({
                    icon: 'error',
                    title: 'Error!',
                    text: 'Cannot update status. Missing data. Please refresh and try again.',
                    timer: 3000,
                    showConfirmButton: false
                });
                return;
            }

            statusUpdatingSpinner.style.display = 'inline-block';
            dropdownOrderStatus.disabled = true;

            const csrftoken = getCookie('csrftoken');

            fetch(updateStatusUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    order_id: orderId,
                    status: newStatus
                })
            })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(err => { throw new Error(err.message || 'Server error'); });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            icon: 'success',
                            title: data.success_title || 'Success!',
                            text: data.message || 'Order status updated successfully.',
                            showConfirmButton: false,
                            timer: 3000
                        }).then(() => {
                            location.reload();
                        });
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error!',
                            text: data.message || 'Failed to update order status.',
                            timer: 3000,
                            showConfirmButton: false
                        });
                    }
                })
                .catch(error => {
                    console.error('Error updating order status:', error);
                    Swal.fire({
                        icon: 'error',
                        title: 'Network Error!',
                        text: `Failed to update status: ${error.message}. Please check your connection.`,
                        timer: 3000,
                        showConfirmButton: false
                    });
                })
                .finally(() => {
                    statusUpdatingSpinner.style.display = 'none';
                    dropdownOrderStatus.disabled = false;
                });
        }
    });

    orderDetailsModal.addEventListener('hidden.bs.modal', function () {
        modalOrderId.textContent = '0000';
        modalOrderFullName.textContent = '';
        modalOrderPhoneNumber.textContent = '';
        modalOrderWilaya.textContent = '';
        modalOrderCommune.textContent = '';
        modalProductName.textContent = '';
        modalProductPrice.textContent = '';
        modalOrderQuantity.textContent = '';
        modalOrderTotalPrice.textContent = '';
        modalOrderCreatedAt.textContent = '';

        modalOrderStatusText.textContent = '';
        dropdownOrderStatus.className = 'btn btn-sm dropdown-toggle';
        modalStatusDropdownMenu.innerHTML = '';
        statusUpdatingSpinner.style.display = 'none';

        modalContent.style.display = 'none';
        modalError.style.display = 'none';
        modalLoadingSpinner.style.display = 'block';
    });
    // --- END: Order Details Modal related code ---

}); // End of the single DOMContentLoaded listener for the entire script