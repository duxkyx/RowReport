document.addEventListener('DOMContentLoaded', function () {
  const modalEl = document.getElementById('uploadSessionModal');
  if (!modalEl) return;

  const form = modalEl.querySelector('form');
  const uploadBtn = form.querySelector('#uploadBtn');

  // Initialize Select2 when modal is shown
  modalEl.addEventListener('shown.bs.modal', function () {    
    $('.user-dropdown').select2({
      placeholder: "Search for a user",
      ajax: {
        url: getUsersApiRoute,
        dataType: 'json',
        delay: 250,
        data: function (params) { return { order: params.term }; },
        processResults: function (data) {
          return {
            results: data.map(user => ({
              id: user.id,
              text: `${user.first_name} ${user.last_name} (${user.email})`
            }))
          };
        },
        cache: true
      },
      minimumInputLength: 0,
      dropdownParent: $('#uploadSessionModal')
    });
  });

  // Show modal if flag is set
  if(showUploadModal) {
    if(modalEl){ 
        document.getElementById('loading-overlay').style.display = 'none';
        // Show Bootstrap modal
        const myModal = new bootstrap.Modal(modalEl, {});
        myModal.show();
    }
  }
  
  // Reset button when modal closes
  modalEl.addEventListener('hidden.bs.modal', function () {
    uploadBtn.disabled = false;
    uploadBtn.innerText = 'Upload';
  });
});
