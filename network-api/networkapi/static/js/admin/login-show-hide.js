const admin = document.querySelector('div.admin-access');
const google = document.querySelector('form div.social-login');

const toggle = document.querySelector('button.admin-login');
toggle.addEventListener( "click", function(evt) {
  [admin, google].forEach( function(e) {
    e.classList.toggle("hidden");
  });
});

