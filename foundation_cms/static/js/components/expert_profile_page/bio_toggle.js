const SELECTORS = {
  bio: "[data-expert-profile-bio]",
  image: ".expert-profile-intro__image",
  toggle: "[data-expert-profile-bio-toggle]",
};

const COLLAPSED_CLASS = "expert-profile-intro__bio--collapsed";
const COLLAPSED_TOGGLE_CLASS = "expert-profile-intro__bio-toggle--collapsed";
const COLLAPSED_HEIGHT_PROPERTY = "--expert-profile-bio-collapsed-height";
const TOGGLE_LEFT_PROPERTY = "--expert-profile-bio-toggle-left";
const TOGGLE_TOP_PROPERTY = "--expert-profile-bio-toggle-top";
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

function getBoundaryRect(bio, boundary) {
  const range = bio.ownerDocument.createRange();
  range.setStart(bio, 0);
  range.setEnd(boundary.node, boundary.offset);

  const rangeRects = range.getClientRects
    ? Array.from(range.getClientRects()).filter(
        (rect) => rect.width || rect.height,
      )
    : [];
  return rangeRects.at(-1) || range.getBoundingClientRect();
}

function getCollapsedLayout(bio, boundary, container) {
  const boundaryRect = getBoundaryRect(bio, boundary);
  const bioRect = bio.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();
  const toggle = container.querySelector(SELECTORS.toggle);
  const toggleHeight = toggle?.getBoundingClientRect().height || 0;

  return {
    height: Math.ceil(boundaryRect.bottom - bioRect.top),
    left: Math.ceil(boundaryRect.right - containerRect.left),
    top: Math.round(boundaryRect.bottom - toggleHeight - containerRect.top),
  };
}

function getAvailableInlineEnd(container, lineRect) {
  const containerRect = container.getBoundingClientRect();
  const image = container.querySelector(SELECTORS.image);
  if (!image) return containerRect.right;

  const view = container.ownerDocument.defaultView;
  const imageStyle = view.getComputedStyle(image);
  const imageRect = image.getBoundingClientRect();
  const overlapsLine =
    lineRect.bottom > imageRect.top && lineRect.top < imageRect.bottom;
  if (imageStyle.float !== "right" || !overlapsLine) {
    return containerRect.right;
  }

  const imageMarginLeft = Number.parseFloat(imageStyle.marginLeft) || 0;
  return Math.min(containerRect.right, imageRect.left - imageMarginLeft);
}

function getFittingCollapseBoundary(bio, boundary, toggle, container) {
  const { text, positions } = getVisibleTextMap(bio);
  let boundaryIndex = positions.findIndex(
    (position) =>
      position.node === boundary.node && position.offset === boundary.offset,
  );
  if (boundaryIndex < 0) return boundary;

  const view = bio.ownerDocument.defaultView;
  const toggleStyle = view.getComputedStyle(toggle);
  const toggleWidth = toggle.getBoundingClientRect().width;
  const toggleGap = Number.parseFloat(toggleStyle.marginLeft) || 0;

  while (boundaryIndex >= 0) {
    const candidate = positions[boundaryIndex];
    const lineRect = getBoundaryRect(bio, candidate);
    const inlineEnd = getAvailableInlineEnd(container, lineRect);

    if (lineRect.right + toggleGap + toggleWidth <= inlineEnd) {
      return candidate;
    }

    const previousSpace = text.lastIndexOf(" ", boundaryIndex - 1);
    boundaryIndex = previousSpace > 0 ? previousSpace - 1 : boundaryIndex - 1;
  }

  return positions[0];
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

  const setCollapsed = (isCollapsed) => {
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

  const cleanup = () => {
    setCollapsed(false);
    const parents = new Set();
    overflowWrappers.forEach((wrapper) => {
      const parent = wrapper.parentNode;
      if (!parent) return;
      parents.add(parent);
      wrapper.replaceWith(...wrapper.childNodes);
    });
    parents.forEach((parent) => parent.normalize());
  };

  return { cleanup, setCollapsed };
}

export function initExpertProfileBioToggle() {
  const bio = document.querySelector(SELECTORS.bio);
  const toggle = document.querySelector(SELECTORS.toggle);
  if (!bio || !toggle) return;
  const container = toggle.parentElement;
  if (!container) return;
  const toggleLabel = toggle.querySelector(
    "[data-expert-profile-bio-toggle-label]",
  );
  if (!toggleLabel) return;

  const limit = Number.parseInt(bio.dataset.collapsedCharLimit, 10);
  if (!Number.isFinite(limit) || limit < 1) return;

  const initialBoundary = getBioCollapseBoundary(bio, limit);
  if (!initialBoundary) return;

  let overflow = null;
  const applyCollapsedLayout = () => {
    overflow?.cleanup();
    overflow = null;
    bio.classList.remove(COLLAPSED_CLASS);
    toggle.hidden = false;
    toggle.classList.add(COLLAPSED_TOGGLE_CLASS);

    const boundary = getFittingCollapseBoundary(
      bio,
      getBioCollapseBoundary(bio, limit),
      toggle,
      container,
    );
    const layout = getCollapsedLayout(bio, boundary, container);
    bio.style.setProperty(COLLAPSED_HEIGHT_PROPERTY, `${layout.height}px`);
    toggle.style.setProperty(TOGGLE_LEFT_PROPERTY, `${layout.left}px`);
    toggle.style.setProperty(TOGGLE_TOP_PROPERTY, `${layout.top}px`);
    overflow = prepareSemanticOverflow(bio, boundary);
    bio.classList.add(COLLAPSED_CLASS);
    overflow.setCollapsed(true);
  };

  const remeasureCollapsedLayout = () => {
    if (bio.isConnected && toggle.getAttribute("aria-expanded") === "false") {
      applyCollapsedLayout();
    }
  };

  applyCollapsedLayout();

  const fonts = bio.ownerDocument.fonts;
  fonts?.ready?.then(remeasureCollapsedLayout);
  fonts?.addEventListener?.("loadingdone", remeasureCollapsedLayout);

  toggle.addEventListener("click", () => {
    const isExpanded = toggle.getAttribute("aria-expanded") === "true";
    const nextExpanded = !isExpanded;

    if (nextExpanded) {
      bio.classList.remove(COLLAPSED_CLASS);
      toggle.classList.remove(COLLAPSED_TOGGLE_CLASS);
      overflow?.setCollapsed(false);
    } else {
      applyCollapsedLayout();
    }
    toggle.setAttribute("aria-expanded", `${nextExpanded}`);
    toggleLabel.textContent = nextExpanded
      ? toggle.dataset.showLessLabel
      : toggle.dataset.showMoreLabel;
  });

  window.addEventListener("resize", () => {
    remeasureCollapsedLayout();
  });
}
