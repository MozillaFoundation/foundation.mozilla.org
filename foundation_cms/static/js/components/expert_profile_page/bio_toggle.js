const SELECTORS = {
  bio: "[data-expert-profile-bio]",
  toggle: "[data-expert-profile-bio-toggle]",
};

const COLLAPSED_CLASS = "expert-profile-intro__bio--collapsed";
const COLLAPSED_HEIGHT_PROPERTY = "--expert-profile-bio-collapsed-height";
const OVERFLOW_ATTRIBUTE = "data-expert-profile-bio-overflow";

function getVisibleTextMap(bio) {
  const characters = [];
  const positions = [];
  const roots = bio.children.length ? Array.from(bio.children) : [bio];
  const nodeFilter = bio.ownerDocument.defaultView.NodeFilter;

  roots.forEach((root, rootIndex) => {
    const walker = bio.ownerDocument.createTreeWalker(
      root,
      nodeFilter.SHOW_TEXT,
    );
    let textNode = walker.nextNode();
    let pendingSpace = rootIndex > 0 && characters.length > 0;

    while (textNode) {
      for (let index = 0; index < textNode.data.length; index += 1) {
        const character = textNode.data[index];
        if (/\s/u.test(character)) {
          pendingSpace = characters.length > 0;
          continue;
        }

        if (pendingSpace) {
          characters.push(" ");
          positions.push({ node: textNode, offset: index });
          pendingSpace = false;
        }

        characters.push(character);
        positions.push({ node: textNode, offset: index + 1 });
      }
      textNode = walker.nextNode();
    }
  });

  return { text: characters.join(""), positions };
}

export function getBioCollapseBoundary(bio, limit) {
  const { text, positions } = getVisibleTextMap(bio);
  if (text.length <= limit) return null;

  const candidate = text.slice(0, limit + 1);
  const wordBoundary = candidate.lastIndexOf(" ");
  const cutoff = wordBoundary > 0 ? wordBoundary : limit;

  return positions[cutoff - 1];
}

function getCollapsedHeight(bio, boundary) {
  const range = bio.ownerDocument.createRange();
  range.setStart(bio, 0);
  range.setEnd(boundary.node, boundary.offset);

  const height =
    range.getBoundingClientRect().bottom - bio.getBoundingClientRect().top;
  return Math.ceil(height);
}

function restoreAttribute(element, name, value) {
  if (value === null) element.removeAttribute(name);
  else element.setAttribute(name, value);
}

function prepareSemanticOverflow(bio, boundary) {
  const view = bio.ownerDocument.defaultView;
  const walker = bio.ownerDocument.createTreeWalker(
    bio,
    view.NodeFilter.SHOW_TEXT,
  );
  const textNodes = [];
  let textNode = walker.nextNode();
  while (textNode) {
    textNodes.push(textNode);
    textNode = walker.nextNode();
  }

  const boundaryIndex = textNodes.indexOf(boundary.node);
  const overflowNodes = textNodes.slice(boundaryIndex + 1);
  if (boundary.offset < boundary.node.data.length) {
    overflowNodes.unshift(boundary.node.splitText(boundary.offset));
  }

  const overflowWrappers = overflowNodes
    .filter((node) => node.data.trim())
    .map((node) => {
      const wrapper = bio.ownerDocument.createElement("span");
      wrapper.setAttribute(OVERFLOW_ATTRIBUTE, "");
      node.parentNode.insertBefore(wrapper, node);
      wrapper.append(node);
      return wrapper;
    });
  const followsBoundary = (element) =>
    Boolean(
      boundary.node.compareDocumentPosition(element) &
      view.Node.DOCUMENT_POSITION_FOLLOWING,
    );
  const postBoundaryElements = Array.from(bio.querySelectorAll("*")).filter(
    (element) =>
      !element.hasAttribute(OVERFLOW_ATTRIBUTE) && followsBoundary(element),
  );
  const postBoundaryElementSet = new Set(postBoundaryElements);
  const overflowRoots = [
    ...overflowWrappers,
    ...postBoundaryElements.filter(
      (element) => !postBoundaryElementSet.has(element.parentElement),
    ),
  ];
  const overflowStates = new Map(
    overflowRoots.map((element) => [
      element,
      {
        ariaHidden: element.getAttribute("aria-hidden"),
        inert: element.getAttribute("inert"),
      },
    ]),
  );

  return (isCollapsed) => {
    overflowStates.forEach((state, element) => {
      if (isCollapsed) {
        element.setAttribute("aria-hidden", "true");
        element.setAttribute("inert", "");
      } else {
        restoreAttribute(element, "aria-hidden", state.ariaHidden);
        restoreAttribute(element, "inert", state.inert);
      }
    });
  };
}

export function initExpertProfileBioToggle() {
  const bio = document.querySelector(SELECTORS.bio);
  const toggle = document.querySelector(SELECTORS.toggle);
  if (!bio || !toggle) return;

  const limit = Number.parseInt(bio.dataset.collapsedCharLimit, 10);
  if (!Number.isFinite(limit) || limit < 1) return;

  const boundary = getBioCollapseBoundary(bio, limit);
  if (!boundary) return;

  const updateOverflowAccessibility = prepareSemanticOverflow(bio, boundary);

  const updateCollapsedHeight = () => {
    const wasCollapsed = bio.classList.contains(COLLAPSED_CLASS);
    bio.classList.remove(COLLAPSED_CLASS);
    const height = getCollapsedHeight(bio, boundary);
    bio.style.setProperty(COLLAPSED_HEIGHT_PROPERTY, `${height}px`);
    bio.classList.toggle(COLLAPSED_CLASS, wasCollapsed);
  };

  updateCollapsedHeight();
  bio.classList.add(COLLAPSED_CLASS);
  updateOverflowAccessibility(true);
  toggle.hidden = false;

  toggle.addEventListener("click", () => {
    const isExpanded = toggle.getAttribute("aria-expanded") === "true";
    const nextExpanded = !isExpanded;

    if (!nextExpanded) updateCollapsedHeight();
    bio.classList.toggle(COLLAPSED_CLASS, !nextExpanded);
    updateOverflowAccessibility(!nextExpanded);
    toggle.setAttribute("aria-expanded", `${nextExpanded}`);
    toggle.textContent = nextExpanded
      ? toggle.dataset.showLessLabel
      : toggle.dataset.showMoreLabel;
  });

  window.addEventListener("resize", updateCollapsedHeight);
}
