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
    notificationPopup.classList.toggle('show');
    accountPopup.classList.remove('show');
    popupOverlay.style.display = notificationPopup.classList.contains('show') ? 'block' : 'none';
});

accountBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    accountPopup.classList.toggle('show');
    notificationPopup.classList.remove('show');
    popupOverlay.style.display = accountPopup.classList.contains('show') ? 'block' : 'none';
});

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
document.addEventListener('click', function(event) {
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

markAllRead.addEventListener('click', function () {
    unreadNotifications.forEach(notification => {
        notification.classList.remove('notification-unread');
    });
    notificationBadge.textContent = '0';
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
