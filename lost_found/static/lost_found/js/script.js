// --- AUTH MODAL LOGIC ---
document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle for login modal
    var passwordInput = document.getElementById('modal-login-password');
    var togglePassword = document.getElementById('toggle-password-visibility');
    var eyeIcon = document.getElementById('eye-icon');
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            var isHidden = passwordInput.type === 'password';
            passwordInput.type = isHidden ? 'text' : 'password';
            if (eyeIcon) {
                eyeIcon.style.opacity = isHidden ? 1 : 0.7;
            }
        });
    }

            // --- REPORT LOST ITEM MODAL LOGIC ---
            var reportLostModal = document.getElementById('report-lost-modal');
            var reportLostModalClose = document.getElementById('report-lost-modal-close');
            function openReportLostModal() {
                if (reportLostModal) {
                    reportLostModal.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            }
            function closeReportLostModal() {
                if (reportLostModal) {
                    reportLostModal.classList.remove('open');
                    document.body.style.overflow = '';
                }
            }
            if (reportLostModalClose) {
                reportLostModalClose.addEventListener('click', closeReportLostModal);
            }
            if (reportLostModal) {
                reportLostModal.addEventListener('click', function(e) {
                    if (e.target === reportLostModal) closeReportLostModal();
                });
            }
            window.openReportLostModal = openReportLostModal;
            window.closeReportLostModal = closeReportLostModal;
            var reportFoundModal = document.getElementById('report-found-modal');
            var reportFoundModalClose = document.getElementById('report-found-modal-close');
            function openReportFoundModal() {
                if (reportFoundModal) {
                    reportFoundModal.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            }
            function closeReportFoundModal() {
                if (reportFoundModal) {
                    reportFoundModal.classList.remove('open');
                    document.body.style.overflow = '';
                }
            }
            if (reportFoundModalClose) {
                reportFoundModalClose.addEventListener('click', closeReportFoundModal);
            }
            if (reportFoundModal) {
                reportFoundModal.addEventListener('click', function(e) {
                    if (e.target === reportFoundModal) closeReportFoundModal();
                });
            }
            window.openReportFoundModal = openReportFoundModal;
            window.closeReportFoundModal = closeReportFoundModal;
            var adminReportFoundModal = document.getElementById('admin-report-found-modal');
            var adminReportFoundModalClose = document.getElementById('admin-report-found-modal-close');
            function openAdminReportFoundModal() {
                if (adminReportFoundModal) {
                    adminReportFoundModal.classList.add('open');
                    document.body.style.overflow = 'hidden';
                }
            }
            function closeAdminReportFoundModal() {
                if (adminReportFoundModal) {
                    adminReportFoundModal.classList.remove('open');
                    document.body.style.overflow = '';
                }
            }
            if (adminReportFoundModalClose) {
                adminReportFoundModalClose.addEventListener('click', closeAdminReportFoundModal);
            }
            if (adminReportFoundModal) {
                adminReportFoundModal.addEventListener('click', function(e) {
                    if (e.target === adminReportFoundModal) closeAdminReportFoundModal();
                });
            }
            window.openAdminReportFoundModal = openAdminReportFoundModal;
            window.closeAdminReportFoundModal = closeAdminReportFoundModal;
        // --- CLAIM BUTTONS LOGIC ---
        var claimModal = document.getElementById('claim-modal');
        var claimModalClose = document.getElementById('claim-modal-close');
        var claimItemIdInput = document.getElementById('claim-item-id');
        // Open claim modal (optionally with item id)
        function openClaimModal(itemId) {
            if (claimModal) {
                claimModal.classList.add('open');
                document.body.style.overflow = 'hidden';
                if (claimItemIdInput) {
                    claimItemIdInput.value = itemId || '';
                }
            }
        }
        // Close claim modal
        function closeClaimModal() {
            if (claimModal) {
                claimModal.classList.remove('open');
                document.body.style.overflow = '';
                if (claimItemIdInput) {
                    claimItemIdInput.value = '';
                }
            }
        }
        // Hero section 'Claim an Item' button
        var claimHeroBtn = document.getElementById('claim-item-btn');
        var reportLostBtn = document.getElementById('report-lost-btn');
        if (claimHeroBtn) {
            claimHeroBtn.addEventListener('click', function(e) {
                e.preventDefault();
                var foundTabBtn = document.getElementById('found-tab-btn');
                var foundSection = document.getElementById('found-items-section');
                var lostSection = document.getElementById('lost-items-section');
                var lostTabBtn = document.getElementById('lost-tab-btn');

                if (foundTabBtn && foundSection && lostSection && lostTabBtn) {
                    foundSection.style.display = 'block';
                    lostSection.style.display = 'none';
                    foundTabBtn.classList.add('active');
                    lostTabBtn.classList.remove('active');
                    foundSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    return;
                }

                openClaimModal();
            });
        }
        if (reportLostBtn) {
            reportLostBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openReportLostModal();
            });
        }
        var reportFoundBtn = document.getElementById('report-found-btn');
        if (reportFoundBtn) {
            reportFoundBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openReportFoundModal();
            });
        }
        var adminReportFoundBtn = document.getElementById('admin-report-found-btn');
        if (adminReportFoundBtn) {
            adminReportFoundBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openAdminReportFoundModal();
            });
        }
        var reportLostTriggers = document.querySelectorAll('.report-lost-modal-trigger');
        reportLostTriggers.forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                openReportLostModal();
            });
        });
        var reportFoundTriggers = document.querySelectorAll('.report-found-modal-trigger');
        reportFoundTriggers.forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                openReportFoundModal();
            });
        });
        var adminReportFoundTriggers = document.querySelectorAll('.admin-report-found-modal-trigger');
        adminReportFoundTriggers.forEach(function(trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                openAdminReportFoundModal();
            });
        });
        // 'Claim This Item' buttons on found cards
        var claimBtns = document.querySelectorAll('.claim-btn');
        claimBtns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                openClaimModal(btn.dataset.itemId);
            });
        });
        // Close claim modal on close button
        if (claimModalClose) {
            claimModalClose.addEventListener('click', closeClaimModal);
        }
        // Close claim modal on overlay click
        if (claimModal) {
            claimModal.addEventListener('click', function(e) {
                if (e.target === claimModal) closeClaimModal();
            });
        }
        window.openClaimModal = openClaimModal;
        window.closeClaimModal = closeClaimModal;
    // Open modal on Login link click
    function openAuthModal() {
        document.getElementById('auth-modal').classList.add('open');
        document.body.style.overflow = 'hidden';
    }
    function closeAuthModal() {
        document.getElementById('auth-modal').classList.remove('open');
        document.body.style.overflow = '';
    }
    // Logo click triggers login modal (desktop & mobile)
    var logoTriggers = document.querySelectorAll('.login-logo-trigger, .auth-modal-trigger');
    logoTriggers.forEach(function(logo) {
        logo.addEventListener('click', function(e) {
            e.preventDefault();
            openAuthModal();
        });
    });
    // Close modal
    var closeBtn = document.getElementById('auth-modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeAuthModal);
    }
    // Tab switching
    var loginTab = document.getElementById('login-tab');
    var registerTab = document.getElementById('register-tab');
    var loginForm = document.getElementById('login-form-container');
    var registerForm = document.getElementById('register-form-container');
    if (loginTab && registerTab && loginForm && registerForm) {
        loginTab.addEventListener('click', function() {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            loginForm.style.display = '';
            registerForm.style.display = 'none';
        });
        registerTab.addEventListener('click', function() {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            registerForm.style.display = '';
            loginForm.style.display = 'none';
        });
    }
    // Close modal on overlay click
    var modal = document.getElementById('auth-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeAuthModal();
        });
    }
    // Helper to close mobile nav
    function closeMobileNav() {
        var overlay = document.getElementById('mobile-nav-overlay');
        var hamburger = document.getElementById('hamburger-menu');
        if (overlay && hamburger) {
            overlay.classList.remove('open');
            hamburger.style.display = 'flex';
            document.body.style.overflow = '';
        }
    }
});
// Hamburger menu toggle for mobile overlay
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger-menu');
    const overlay = document.getElementById('mobile-nav-overlay');
    const closeBtn = document.getElementById('close-mobile-nav');
    if (hamburger && overlay && closeBtn) {
        hamburger.addEventListener('click', function() {
            overlay.classList.add('open');
            hamburger.style.display = 'none';
            document.body.style.overflow = 'hidden';
        });
        closeBtn.addEventListener('click', function() {
            overlay.classList.remove('open');
            hamburger.style.display = 'flex';
            document.body.style.overflow = '';
        });
    }
});
function updateFileName(input) {
    const fileNameDisplay = document.getElementById('file-name');
    const previewContainer = document.getElementById('image-preview'); // Dagdagan mo ng div sa HTML
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // Pinapakita yung picture bago i-submit
            previewContainer.innerHTML = `<img src="${e.target.result}" style="max-height: 150px; border-radius: 8px; margin-top: 10px;">`;
        }
        
        reader.readAsDataURL(input.files[0]);
        fileNameDisplay.innerText = "File Selected: " + input.files[0].name;
    }
}
