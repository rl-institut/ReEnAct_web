/* Project specific Javascript goes here. */

document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('welcome-banner');
    const closeButton = document.getElementById('close-banner');

    if (banner && closeButton) {
        // Show the banner when the page is loaded
        banner.style.display = 'flex';

        closeButton.addEventListener('click', function() {
            banner.style.display = 'none';
        });

        // Also close when clicking outside the banner content
        banner.addEventListener('click', function(event) {
            if (event.target === banner) {
                banner.style.display = 'none';
            }
        });
    }
});
