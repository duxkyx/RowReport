document.addEventListener('DOMContentLoaded', function() {
    const modalEl = document.getElementById('uploadSessionModal');
    const file_upload_form = document.querySelector('form');
    const modal_Form = modalEl.querySelector('form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');

    // Show loading overlay on file upload form submit
    if(file_upload_form) {
        file_upload_form.addEventListener('submit', function(e) {
            loadingOverlay.style.display = 'flex';

            const messages = [
                'Uploading file',
                'Reading file',
                'Gridding data',
                'Initiating objects',
                'Iterating athletes',
                'Seperating strokes',
                'Calculating values',
                'Mapping data',
                'Converting units',
                'Calculating syncronicity',
                'Returning profiles',
                'Caching results',
                'Looping until finished'
            ];

            let i = 0;
            setInterval(() => {
                loadingText.textContent = messages[i];
                i = (i + 1) % messages.length;
            }, 3500);
        });
    }

    // Initialize uploading spinner and disable button on submit
    let clickedButton = null;

    // Track which button was clicked
    modal_Form.querySelectorAll('button[type="submit"]').forEach(btn => {
        btn.addEventListener('click', function () {
        clickedButton = btn;
        });
    });

    modal_Form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!clickedButton) return; // Safety check

        // Disable the button
        clickedButton.disabled = true;
        clickedButton.innerText = 'Uploading...';
        loadingText.innerText = 'Uploading session';

        // Hide modal
        const bsModal = bootstrap.Modal.getOrCreateInstance(modalEl);
        bsModal.hide();

        // Show full-page spinner overlay
        loadingOverlay.style.display = 'flex';

        // Create a hidden input with the button value so Flask sees it
        const tempInput = document.createElement('input');
        tempInput.type = 'hidden';
        tempInput.name = clickedButton.name;
        tempInput.value = clickedButton.value;
        modal_Form.appendChild(tempInput);

        // Submit after a short delay
        setTimeout(() => modal_Form.submit(), 50);
    });
});