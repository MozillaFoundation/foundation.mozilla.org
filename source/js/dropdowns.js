const Dropdowns = {
  init: function () {
    // Toggle dropdowns when dropdown is clicked
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    for (let i = 0; i < dropdowns.length; i++) {
      const element = dropdowns[i];
      element.addEventListener('click', function(e) {
        e.preventDefault()
        element.classList.toggle("show")
        const id = element.id
        const target = document.querySelector(`[aria-labelledby="${id}"]`)
        target.classList.toggle("d-block")
      })
    }

    // Close dropdowns when item is clicked
    const dropdownItems = document.querySelectorAll('.dropdown-item')
    for (let i = 0; i < dropdownItems.length; i++) {
      const item = dropdownItems[i];
      item.addEventListener('click', function() {
        item.parentElement.classList.remove('d-block', 'show')
      })
    }
  },
};

export default Dropdowns;
