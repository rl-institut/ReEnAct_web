/* Project specific Javascript goes here. */

document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('welcome-banner');
    const closeButton = document.getElementById('close-banner');
    const startTutorialBtn = document.getElementById('start-tutorial');
    const welcomeContent = document.getElementById('welcome-content');
    const tutorialContainer = document.getElementById('tutorial-container');

    let currentStep = 1; // 1-based indexing matching element ids

    function showBanner() {
        if (banner) banner.style.display = 'flex';
    }

    function hideBanner() {
        if (banner) banner.style.display = 'none';
        // reset tutorial state for next open
        if (tutorialContainer) tutorialContainer.classList.add('hidden');
        if (welcomeContent) welcomeContent.style.display = '';
        hideAllSteps();
        currentStep = 1;
    }

    function hideAllSteps() {
        const steps = document.querySelectorAll('.tutorial-step');
        steps.forEach(el => el.classList.add('hidden'));
    }

    function showStep(stepNumber) {
        hideAllSteps();
        const stepEl = document.getElementById(`tutorial-step-${stepNumber}`);
        if (stepEl) stepEl.classList.remove('hidden');
        currentStep = stepNumber;
    }

    function startTutorial() {
        if (!tutorialContainer || !welcomeContent) return;
        welcomeContent.style.display = 'none';
        tutorialContainer.classList.remove('hidden');
        showStep(1);
        attachStepHandlers();
    }

    function attachStepHandlers() {
        // Next buttons
        const nextButtons = tutorialContainer.querySelectorAll('.next-step');
        nextButtons.forEach(btn => {
            btn.onclick = function() {
                const next = currentStep + 1;
                const nextEl = document.getElementById(`tutorial-step-${next}`);
                if (nextEl) {
                    showStep(next);
                } else {
                    finishTutorial();
                }
            }
        });

        // Close buttons inside tutorial
        const closeBtns = tutorialContainer.querySelectorAll('.close-tutorial');
        closeBtns.forEach(btn => {
            btn.onclick = function() { hideBanner(); };
        });

        // Finish button (last step)
        const finishBtn = document.getElementById('finish-tutorial');
        if (finishBtn) finishBtn.onclick = function() { finishTutorial(); };
    }

    function finishTutorial() {
        hideBanner();
    }

    if (banner) {
        // Show banner on load
        showBanner();

        if (closeButton) {
            closeButton.addEventListener('click', function() {
                hideBanner();
            });
        }

        if (startTutorialBtn) {
            startTutorialBtn.addEventListener('click', function() {
                startTutorial();
            });
        }

        // Also close when clicking outside the banner content (only if click directly on overlay)
        banner.addEventListener('click', function(event) {
            if (event.target === banner) {
                hideBanner();
            }
        });
    }
});
