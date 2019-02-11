// find all of the buttons~
let filters = document.querySelectorAll('.cms .profile-directory .profile-filters .filter-button');

// Aaaan add a silly event handler to each
Array.from(filters).forEach(button => {
  button.addEventListener("click", evt => {
    // I considered using alert. Let's not talk about it.
    console.log(button.textContent);
  });
});
