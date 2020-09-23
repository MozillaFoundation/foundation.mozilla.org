const Dropdowns = {
  init: function() {
    // Toggle dropdowns when dropdown is clicked
    document.querySelectorAll(".dropdown-toggle").forEach(element =>
      element.addEventListener("click", _ => {
        element.classList.toggle("show");
        const target = document.querySelector(
          `[aria-labelledby="${element.id}"]`
        );
        target.classList.toggle("d-block");
      })
    );

    // Close dropdowns when item is clicked
    document.querySelectorAll(".dropdown-item").forEach(element => {
      element.addEventListener("click", _ => {
        element.parentElement.classList.remove("d-block", "show");
      });
    });
  }
};

export default Dropdowns;
