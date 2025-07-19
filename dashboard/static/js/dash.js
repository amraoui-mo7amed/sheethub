// Toggle sidebar on mobile
const menuToggle = document.getElementById('menuToggle');
if (menuToggle) {
    menuToggle.addEventListener('click', function () {
        document.querySelector('.sidebar').classList.toggle('active');
    });

}

// Notification and account popup toggles
const notificationBtn = document.getElementById('notificationBtn');
const notificationPopup = document.getElementById('notificationPopup');
const accountBtn = document.getElementById('accountBtn');
const accountPopup = document.getElementById('accountPopup');
const popupOverlay = document.getElementById('popupOverlay');

notificationBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    // Toggle the notification popup
    const isShowing = !notificationPopup.classList.contains('show');
    notificationPopup.classList.toggle('show');
    accountPopup.classList.remove('show');
    popupOverlay.style.display = isShowing ? 'block' : 'none';

    // If showing notifications, fetch the latest ones
    if (isShowing) {
        fetchNotifications();
    }
});

accountBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    accountPopup.classList.toggle('show');
    notificationPopup.classList.remove('show');
    popupOverlay.style.display = accountPopup.classList.contains('show') ? 'block' : 'none';
});

// Function to fetch notifications from the server
function fetchNotifications() {
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationList = document.querySelector('.notification-list');
    const notificationBadge = document.querySelector('.notification-badge');

    if (!notificationBtn || !notificationList) return;

    const url = notificationBtn.getAttribute('data-target-url');

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'same-origin'
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Clear existing notifications
            notificationList.innerHTML = '';

            if (data.error) {
                // Handle case where no notifications are found
                notificationList.innerHTML = `
                <div class="text-center p-4 text-muted">
                    ${data.error}
                </div>
            `;
                if (notificationBadge) {
                    notificationBadge.style.display = 'none';
                }
                return;
            }

            if (data.notifications && data.notifications.length > 0) {
                // Update notification badge count (unread notifications)
                const unreadCount = data.notifications.filter(n => !n.is_read).length;
                const notificationBadge = notificationBtn.querySelector('.notification-badge') ||
                    document.createElement('span');

                if (!notificationBadge.classList.contains('notification-badge')) {
                    notificationBadge.className = 'notification-badge';
                    notificationBtn.appendChild(notificationBadge);
                }

                notificationBadge.textContent = unreadCount > 0 ? unreadCount : '';
                notificationBadge.style.display = unreadCount > 0 ? 'flex' : 'none';

                // Add each notification to the list
                data.notifications.forEach(notification => {
                    const notificationItem = document.createElement('div');
                    notificationItem.className = `notification-item ${!notification.is_read ? 'notification-unread' : ''}`;
                    notificationItem.innerHTML = `
                        <div class="notification-icon">
                            <i class="fas fa-bell"></i>
                        </div>
                        <div class="notification-content">
                            <div class="notification-text">
                                <strong>${notification.title}</strong> ${notification.message}
                            </div>
                        </div>
                    `;
                    notificationList.appendChild(notificationItem);
                });
            } else {
                // Show message when there are no notifications
                if (notificationBadge) {
                    notificationBadge.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error fetching notifications:', error);
        });
}

// Handle mark all as read button click
document.addEventListener('click', function (e) {
    const markAllReadBtn = e.target.closest('.mark-all-read');
    if (!markAllReadBtn) return;

    e.preventDefault();
    e.stopPropagation();

    const url = markAllReadBtn.getAttribute('data-target-url');
    const notificationBtn = document.getElementById('notificationBtn');

    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify({})
    })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Failed to mark notifications as read');
            }
            return data;
        })
        .then(data => {
            // Update UI to show all notifications as read
            const unreadItems = document.querySelectorAll('.notification-unread');
            unreadItems.forEach(item => {
                item.classList.remove('notification-unread');
            });

            // Update badge count to 0
            const notificationBadge = notificationBtn ? notificationBtn.querySelector('.notification-badge') : null;
            if (notificationBadge) {
                notificationBadge.style.display = 'none';
                notificationBadge.textContent = '';
            }

            // Show success message from backend
            showToast(data.message || 'Notifications updated', 'success');
        })
        .catch(error => {
            console.error('Error marking notifications as read:', error);
            showToast(error.message || 'Failed to update notifications', 'error');
        });
});

// Helper function to get CSRF token
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

// Helper function to show toast messages
function showToast(message, type = 'info') {
    // Check if toast container exists, if not create it
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.position = 'fixed';
        toastContainer.style.top = '20px';
        toastContainer.style.right = '20px';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    // Add toast to container and set timeout to remove it
    toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.remove();
        // Remove container if it's empty
        if (toastContainer.children.length === 0) {
            toastContainer.remove();
        }
    }, 3000);
}

// Close popups when clicking outside
document.addEventListener('click', function (e) {
    if (!notificationPopup.contains(e.target) && !notificationBtn.contains(e.target)) {
        notificationPopup.classList.remove('show');
    }

    if (!accountPopup.contains(e.target) && !accountBtn.contains(e.target)) {
        accountPopup.classList.remove('show');
    }

    if (!notificationPopup.classList.contains('show') && !accountPopup.classList.contains('show')) {
        popupOverlay.style.display = 'none';
    }
});

// Close sidebar when clicking outside
document.addEventListener('click', function (event) {
    const sidebar = document.querySelector('.sidebar');
    const menuToggleBtn = document.getElementById('menuToggle');
    const overlay = document.getElementById('popupOverlay');

    // Only handle if sidebar exists and is active
    if (sidebar && sidebar.classList.contains('active')) {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnMenuToggle = menuToggleBtn && menuToggleBtn.contains(event.target);

        // Close sidebar if click is outside and not on menu toggle
        if (!isClickInsideSidebar && !isClickOnMenuToggle) {
            sidebar.classList.remove('active');
            if (overlay) {
                overlay.style.display = 'none';
            }
        }
    }
});

// Mark all notifications as read
const markAllRead = document.querySelector('.mark-all-read');
const unreadNotifications = document.querySelectorAll('.notification-unread');
const notificationBadge = document.querySelector('.notification-badge');

markAllRead.addEventListener('click', async function (e) {
    e.preventDefault();
    e.stopPropagation();

    const url = markAllRead.getAttribute('data-target-url');

    // Show loading popup
    Swal.fire({
        title: 'Processing...',
        text: 'Please wait while we update your notifications',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    try {
        // Make the API call
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to update notifications');
        }

        // Update UI
        unreadNotifications.forEach(notification => {
            notification.classList.remove('notification-unread');
        });

        if (notificationBadge) {
            notificationBadge.style.display = 'none';
        }

        // Show success popup
        Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: data.message || 'Notifications marked as read',
            confirmButtonText: 'OK',
            timer: 3000,
            timerProgressBar: true
        });

    } catch (error) {
        console.error('Error marking notifications as read:', error);

        // Show error popup
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message || 'An error occurred while updating notifications',
            confirmButtonText: 'OK'
        });
    }
});



document.addEventListener('DOMContentLoaded', function () {
    // Get the `lang` attribute from the <html> tag
    const lang = document.documentElement.lang || 'en'; // Default to 'en' if not set

    // Define phrases for both languages
    const phrases = {
        en: {
            deleteTitle: 'Are you sure?',
            deleteText: "You won't be able to revert this!",
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'Cancel',
            successTitle: 'Deleted!',
            successText: 'The item has been deleted.',
            errorTitle: 'Error!',
            errorText: 'Failed to delete.',
            genericError: 'An error occurred while deleting .'
        },
        fr: {
            deleteTitle: 'Êtes-vous sûr?',
            deleteText: "Cette action est irréversible!",
            confirmButtonText: 'Oui, supprimer!',
            cancelButtonText: 'Annuler',
            successTitle: 'Supprimé!',
            successText: "L'élément a été supprimé.",
            errorTitle: 'Erreur!',
            errorText: 'Échec de la suppression.',
            genericError: "Une erreur s'est produite lors de la suppression."
        }
    };

    // Get the appropriate phrases based on the `lang` attribute
    const currentPhrases = phrases[lang] || phrases.en;

    // Add event listeners to delete buttons
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const deleteUrl = this.dataset.deleteUrl;
            const csrfToken = this.dataset.csrfToken;

            Swal.fire({
                title: currentPhrases.deleteTitle,
                text: currentPhrases.deleteText,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: 'var(--primary)',
                cancelButtonColor: "var(--accent)",
                confirmButtonText: currentPhrases.confirmButtonText,
                cancelButtonText: currentPhrases.cancelButtonText
            }).then((result) => {
                if (result.isConfirmed) {
                    // Perform the actual delete request
                    fetch(deleteUrl, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json'
                        },
                        credentials: 'include'
                    })
                        .then(response => {
                            if (response.ok) {
                                Swal.fire(
                                    currentPhrases.successTitle,
                                    currentPhrases.successText,
                                    'success'
                                ).then(() => {
                                    // Reload the page or remove the row
                                    window.location.reload();
                                });
                            } else {
                                Swal.fire(
                                    currentPhrases.errorTitle,
                                    currentPhrases.errorText,
                                    'error'
                                );
                            }
                        })
                        .catch(error => {
                            Swal.fire(
                                currentPhrases.errorTitle,
                                currentPhrases.genericError,
                                'error'
                            );
                        });
                }
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL
    const currentUrl = window.location.pathname;

    // Get all nav links
    const navLinks = document.querySelectorAll('.menu-item');

    navLinks.forEach(link => {
        // Check if the data-url matches the current URL
        if (link.getAttribute('data-url') === currentUrl) {
            link.classList.add('active'); // Add active class
        } else {
            link.classList.remove('active'); // Remove active class if not matched
        }
    });
});



function sendActivationEmail() {
    const alertDiv = document.getElementById('emailActivationWarning')
    fetch(alertDiv.getAttribute('data-target-url'), {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: data.message,
                    timer: 3000,
                    showConfirmButton: false
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.message,
                    timer: 3000,
                    showConfirmButton: false
                });
            }
        })
        .catch(() => {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something went wrong. Please try again later.',
                timer: 3000,
                showConfirmButton: false
            });
        });
}

// feedback model 
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('customModal');
    const openBtn = document.getElementById('openModal');
    const closeBtn = modal.querySelector('.close-button');
    const modalContent = modal.querySelector('.custom-modal-content');

    // Open modal
    openBtn.addEventListener('click', () => openModal());

    // Close modal
    closeBtn.addEventListener('click', closeModal);

    // Close on background click
    modal.addEventListener('mousedown', function (e) {
        if (e.target === modal) closeModal();
    });

    // Exit with Esc key
    window.addEventListener('keydown', function (e) {
        if (e.key === "Escape" && modal.classList.contains('show')) closeModal();
    });

    // Keyboard accessible close button
    closeBtn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') closeModal();
    });

    function openModal() {
        modal.classList.add('show');
        document.body.classList.add('modal-open');
        // Focus for accessibility
        setTimeout(() => closeBtn.focus(), 200);
    }

    function closeModal() {
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
    }
});

// feedback form 
document.addEventListener("DOMContentLoaded", function () {
    const feedbackForm = document.getElementById("feedbackForm");
    const feedbackErrors = document.getElementById("feedbackErrors");
    const customModal = document.getElementById("customModal");
    const closeButton = customModal.querySelector(".close-button");



    feedbackForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        feedbackErrors.innerHTML = ""; // Clear old errors

        const formData = new FormData(feedbackForm);

        try {
            const response = await fetch(feedbackForm.getAttribute('data-target-url'), {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: formData,
            });

            const data = await response.json();

            if (!response.ok || data.success === false) {
                const errors = data.errors || ["Unexpected error."];
                for (const error of errors) {
                    const li = document.createElement("li");
                    li.textContent = error;
                    li.classList.add("text-danger", "mb-1");
                    feedbackErrors.appendChild(li);
                }
            } else {
                // Close modal
                customModal.classList.remove('show');
                // Show SweetAlert using backend message
                Swal.fire({
                    icon: "success",
                    title: data.message || "✅ Success",
                    text: "",
                    timer: 2500,
                    showConfirmButton: false,
                });

                feedbackForm.reset();
            }
        } catch (error) {
            console.error("Feedback error:", error);
            const li = document.createElement("li");
            li.textContent = "❌ Server error. Try again.";
            li.classList.add("text-danger");
            feedbackErrors.appendChild(li);
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }
});
