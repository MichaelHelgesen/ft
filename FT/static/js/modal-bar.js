

window.addEventListener("DOMContentLoaded", (event) => {
  barBody = document.querySelector(".bar")
  fetch(`${window.origin}/modal`, {
    method: "GET"
  })
    .then(response => {
      return response.text();
    })
    .then(html => {
      barBody.innerHTML = html;
    })
});


/*     $(window).on('load', function() {
        $('#myModal').modal('show');
    }); */
