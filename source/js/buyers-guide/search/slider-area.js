/**
 * mouse/touch scroll functionality for the category area
 * @param {*} event
 */

const subcategories = document.querySelectorAll(`.subcategories`);
const subContainer = document.querySelector(`.subcategory-header`);
const subClasses = subContainer.classList;

let pos = { left: 0, x: 0 };

function stop(evt) {
  evt.preventDefault();
  evt.stopImmediatePropagation();
}

export function markScrollStart(event) {
  stop(event);
  subClasses.add("cursor-grabbing", "select-none");

  pos = {
    left: subContainer.scrollLeft,
    x: event.clientX,
  };

  [`mousemove`, `touchmove`].forEach((type) =>
    document.addEventListener(type, markScrollMove)
  );

  [`mouseup`, `touchend`, `touchcancel`].forEach((type) =>
    document.addEventListener(type, markScrollEnd)
  );
}

function markScrollMove(event) {
  subcategories.forEach((subcategory) => {
    subcategory.classList.add("pointer-events-none");
  });
  const dx = event.clientX - pos.x;
  subContainer.scrollLeft = pos.left - dx;
}

function markScrollEnd(event) {
  stop(event);

  subcategories.forEach((subcategory) => {
    subcategory.classList.remove("pointer-events-none");
  });

  subClasses.remove("cursor-grabbing", "select-none");

  [`mousemove`, `touchmove`].forEach((type) =>
    document.removeEventListener(type, markScrollMove)
  );

  [`mouseup`, `touchend`, `touchcancel`].forEach((type) =>
    document.removeEventListener(type, markScrollEnd)
  );
}
