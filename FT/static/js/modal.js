

window.addEventListener("DOMContentLoaded", (event) => {
  const myModal = new bootstrap.Modal(document.getElementById('exampleModal'), {
    //keyboard: false,
    backdrop: 'static',
  })
  myModal.toggle()
  modalBody = document.querySelector(".modal-inject")
  fetch(`${window.origin}/modal`, {
    method: "GET"
  })
    .then(response => {
      return response.text();
    })
    .then(html => {
      modalBody.innerHTML = html;
    })
});


/*     $(window).on('load', function() {
        $('#myModal').modal('show');
    }); */