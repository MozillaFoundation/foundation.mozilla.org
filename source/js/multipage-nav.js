/**
 * Inject mobile version of multipage navs (secondary navs)
 */
export default () => {
  const targetNode = document.querySelector(
    `#multipage-nav-mobile .container .row .col-12`
  );
  const multipageLinks = document.querySelectorAll(`#multipage-nav a`);

  // if there is no multipage nav, return early
  if (!targetNode) {
    return;
  }

  // if there are no multipage links, remove the parent multipage nav #multipage-nav-mobile and return early
  if (!multipageLinks.length) {
    let parent = targetNode.parentNode;
    while (parent) {
      if (parent.id === `multipage-nav-mobile`) {
        parent.remove();
        break;
      }
      parent = parent.parentNode;
    }

    return;
  }

  let activeLinkLabel = window.gettext("Navigate to...");

  let links = Array.from(multipageLinks).map((link) => {
    const [href, isActive] = [
      link.getAttribute(`href`),
      !!link.getAttribute(`class`).match(/active/),
    ];
    const label = link.dataset.mobile
      ? link.dataset.mobile.trim()
      : link.textContent.trim();

    let className = `multipage-link${isActive ? ` active` : ``}`;

    if (isActive) {
      activeLinkLabel = `<span class="active-link-label d-inline-block ${className}">
            ${label}
          </span>`;
    }

    return `<div><a href="${href}" class="${className}">${label}</a></div>`;
  });

  links.unshift(
    `<div>
        <button class="expander">
          <span class="d-flex justify-content-between">
            <span>${activeLinkLabel}</span>
            <span class="align-self-center control" />
          </span>
        </button>
      </div>`
  );

  targetNode.innerHTML = `<div class="dropdown-nav">${links.join("")}</div>`;

  const dropdown = document.querySelector(`.dropdown-nav`);

  dropdown.querySelector(`.expander`).addEventListener(`click`, (e) => {
    e.preventDefault();
    dropdown.classList.toggle(`dropdown-nav-open`);
  });
};
