/**
 * This handler is used for the PNI Product Page's "dive deeper" component
 * which shows a list of a product's related "news updates".
 *
 * If applicable, the component shows the first 3 items in this list, and gives
 * users the option to expand/collapse the list to show the rest of the items,
 * which we do by toggling a tailwind class that hides any list item after item #3.
 *
 * We also update the "Read more" button's text and icon accordingly.
 */

export default () => {
  const diveDeeperComponent = document.getElementById("dive-deeper");
  const readMoreButton = document.querySelector("#read-more-button");

  if (diveDeeperComponent && readMoreButton) {
    const newsUpdates = diveDeeperComponent.querySelectorAll("ul li");
    let listExpanded = false;

    function toggleListExpansion() {
      if (listExpanded) {
        readMoreButton.querySelector("span").innerText =
          readMoreButton.getAttribute("data-open");
        readMoreButton
          .querySelector("img")
          .classList.replace("-tw-rotate-90", "tw-rotate-90");
      } else {
        readMoreButton.querySelector("span").innerText =
          readMoreButton.getAttribute("data-close");
        readMoreButton
          .querySelector("img")
          .classList.replace("tw-rotate-90", "-tw-rotate-90");
      }

      // Toggling whether or not to hide list items past item #3.
      newsUpdates.forEach((update) => {
        update.classList.toggle("[&:nth-child(n+4)]:tw-hidden");
      });

      listExpanded = !listExpanded;
    }

    readMoreButton.addEventListener("click", toggleListExpansion);
  }
};
