/**
 * Mouse/touch scroll functionality for the sub category area on mobile
 *
 * @todo Rename this file to something more specific. Maybe something like subcategory-scroll.js
 */
const subcategories = document.querySelectorAll(`.subcategories`);
const subContainer = document.querySelector(`.subcategory-header`);
const subClasses = subContainer.classList;

let pos = { left: 0, x: 0 };

function stop(evt) {
  evt.preventDefault();
  evt.stopImmediatePropagation();
}

/**
 * A event handler that initiate the scroll functionality on the sub category area
 *
 * @param {Event} event The event that triggered the function
 */
export function markScrollStart(event) {
  stop(event);
  subClasses.add("cursor-grabbing", "select-none");

  pos = {
    left: subContainer.scrollLeft,
    x: event.clientX,
  };

  document.addEventListener(`mousemove`, markScrollMove);
  document.addEventListener(`mouseup`, markScrollEnd);
}

/**
 * A event handler for moving the scorll on the sub category area
 *
 * @param {Event} event The event that triggered the function
 */
function markScrollMove(event) {
  subcategories.forEach((subcategory) => {
    subcategory.classList.add("pointer-events-none");
  });
  const dx = event.clientX - pos.x;
  subContainer.scrollLeft = pos.left - dx;
}

/**
 * A event handler for stopping the scorll on the sub category area
 *
 * @param {Event} event The event that triggered the function
 */
function markScrollEnd(event) {
  stop(event);

  subcategories.forEach((subcategory) => {
    subcategory.classList.remove("pointer-events-none");
  });

  subClasses.remove("cursor-grabbing", "select-none");

  [`mousemove`].forEach((type) =>
    document.removeEventListener(type, markScrollMove)
  );

  [`mouseup`].forEach((type) =>
    document.removeEventListener(type, markScrollEnd)
  );
}
