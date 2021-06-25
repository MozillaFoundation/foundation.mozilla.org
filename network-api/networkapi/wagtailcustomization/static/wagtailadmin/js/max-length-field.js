/**
 * Event listeners to let editors know when they reached the recommended maximum length of a title.
 * This is paired with max-length-fields.css and wagtailpages/wagtail_hooks.py
 */

 document.addEventListener('DOMContentLoaded', () => {
  const maxLengthFields = document.querySelectorAll(".max-length-warning");

  if(maxLengthFields.length) {
    maxLengthFields.forEach((node) => {
      const parent = node.parentElement;
      const countDown = parent.querySelector('.max-length-countdown');
      const currentCharacters = node.value.length || 0;
      const maxLengthWarning = node.dataset.maxLength;

      countDown.innerHTML = maxLengthWarning - currentCharacters

      if(currentCharacters >= maxLengthWarning) {
        countDown.classList.add("warning")
      }

      node.addEventListener('keyup', event => {
        const totalCharacters = event.target.value.length;
        countDown.innerHTML = maxLengthWarning - totalCharacters;

        if(totalCharacters >= maxLengthWarning) {
          countDown.classList.add("warning")
        } else {
          countDown.classList.remove("warning")
        }
      })
    })
  }
})
