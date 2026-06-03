// Tishyya Client-Side Interactions

document.addEventListener('DOMContentLoaded', function() {
    // 1. Auto-dismiss Alert Messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Apply fade out effect
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // 2. Track Active Navigation Link
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentUrl) {
            link.classList.add('active');
        } else if (currentUrl.startsWith('/products/') && linkPath === '/products/') {
            link.classList.add('active');
        }
    });

    // 3. Highlight dropdown parent if active inside dashboard
    const accountTrigger = document.querySelector('.account-trigger');
    if (accountTrigger && (currentUrl.startsWith('/products/manage/') || currentUrl.startsWith('/login/') || currentUrl.startsWith('/register/'))) {
        accountTrigger.classList.add('active-nav');
    }

    // 4. Click to Toggle Account Submenu
    const accountDropdown = document.querySelector('.account-dropdown');
    if (accountDropdown && accountTrigger) {
        accountTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            accountDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!accountDropdown.contains(e.target)) {
                accountDropdown.classList.remove('active');
            }
        });
    }
});
