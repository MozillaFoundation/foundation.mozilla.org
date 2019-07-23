const copyToClipboard = (linkElement, textToCopy) => {
  let textArea = document.createElement(`textarea`);

  textArea.setAttribute(`contenteditable`, true);
  textArea.setAttribute(`readonly`, false);

  //
  // *** This styling is an extra step which is likely not required. ***
  //
  // Why is it here? To ensure:
  // 1. the element is able to have focus and selection.
  // 2. if element was to flash render it has minimal visual impact.
  // 3. less flakyness with selection and copying which **might** occur if
  //    the textarea element is not visible.
  //
  // The likelihood is the element won't even render, not even a flash,
  // so some of these are just precautions. However in IE the element
  // is visible whilst the popup box asking the user for permission for
  // the web page to copy to the clipboard.
  //

  // Place in top-left corner of screen regardless of scroll position.
  textArea.style.position = `fixed`;
  textArea.style.top = 0;
  textArea.style.left = 0;

  // Ensure it has a small width and height. Setting to 1px / 1em
  // doesn't work as this gives a negative w/h on some browsers.
  textArea.style.width = `2em`;
  textArea.style.height = `2em`;

  // We don't need padding, reducing the size if it does flash render.
  textArea.style.padding = 0;

  // Clean up any borders.
  textArea.style.border = `none`;
  textArea.style.outline = `none`;
  textArea.style.boxShadow = `none`;

  // Avoid flash of white box if rendered for any reason.
  textArea.style.background = `transparent`;

  textArea.value = textToCopy;
  document.body.appendChild(textArea);
  textArea.focus();

  // Simply running textArea.select() and document.execCommand(`copy`) won't work on iOS Safari
  // Below is the suggested solution to make copying and pasting working more cross-platform
  // For details see https://stackoverflow.com/a/34046084
  let range = document.createRange();
  let selection = window.getSelection();

  range.selectNodeContents(textArea);

  selection.removeAllRanges();
  selection.addRange(range);

  textArea.setSelectionRange(0, textArea.value.length);

  try {
    document.execCommand(`copy`);

    let target = linkElement;

    if (target.dataset && target.dataset.successText) {
      let defaultText = target.innerText;

      target.innerText = target.dataset.successText;
      target.classList.add(`copied`);

      setTimeout(() => {
        target.innerText = defaultText;
        target.classList.remove(`copied`);
      }, 3000);
    }
  } catch (err) {
    console.error(`Copy failed.`);
  }

  document.body.removeChild(textArea);
};

export default copyToClipboard;
