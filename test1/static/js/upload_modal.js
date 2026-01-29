var modalEl = document.getElementById('uploadSessionModal');

document.addEventListener('DOMContentLoaded', function () {
  // Ensure the modal exists
  if (!modalEl) return;

  // Attach listener for when modal is shown
  modalEl.addEventListener('shown.bs.modal', function () {    
    $('.user-dropdown').select2({
      placeholder: "Search for a user",
      ajax: {
        url: getUsersApiRoute,
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            order: params.term // search term
          };
        },
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
});

document.addEventListener('DOMContentLoaded', function(){
    if(showUploadModal) {
        if(modalEl){ 
            document.getElementById('loading-overlay').style.display = 'none';
            // Show Bootstrap modal
            const myModal = new bootstrap.Modal(modalEl, {});
            myModal.show();
        }
    }
});
