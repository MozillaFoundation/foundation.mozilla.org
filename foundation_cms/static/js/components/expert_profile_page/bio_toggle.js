const SELECTORS = {
  bio: "[data-expert-profile-bio]",
  toggle: "[data-expert-profile-bio-toggle]",
};

function normalizeVisibleText(value) {
  return value.replace(/\s+/g, " ").trim();
}

function getBioVisibleText(bio) {
  if (!bio.children.length) return bio.textContent;

  return Array.from(bio.children, (child) => child.textContent).join(" ");
}

export function getCollapsedBioText(value, limit) {
  const text = normalizeVisibleText(value);
  if (text.length <= limit) return null;

  const candidate = text.slice(0, limit + 1);
  const wordBoundary = candidate.lastIndexOf(" ");
  const cutoff = wordBoundary > 0 ? wordBoundary : limit;
  return `${candidate.slice(0, cutoff).trimEnd()}…`;
}

export function initExpertProfileBioToggle() {
  const bio = document.querySelector(SELECTORS.bio);
  const toggle = document.querySelector(SELECTORS.toggle);
  if (!bio || !toggle) return;

  const limit = Number.parseInt(bio.dataset.collapsedCharLimit, 10);
  if (!Number.isFinite(limit) || limit < 1) return;

  const collapsedText = getCollapsedBioText(getBioVisibleText(bio), limit);
  if (!collapsedText) return;

  const collapsedBio = document.createElement("div");
  collapsedBio.className = `${bio.className} expert-profile-intro__bio--collapsed`;
  collapsedBio.dataset.expertProfileBioCollapsed = "";
  const paragraph = document.createElement("p");
  paragraph.textContent = collapsedText;
  collapsedBio.append(paragraph);

  bio.before(collapsedBio);
  bio.hidden = true;
  toggle.hidden = false;

  toggle.addEventListener("click", () => {
    const isExpanded = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", `${!isExpanded}`);
    toggle.textContent = isExpanded
      ? toggle.dataset.showMoreLabel
      : toggle.dataset.showLessLabel;
    bio.hidden = isExpanded;
    collapsedBio.hidden = !isExpanded;
  });
}
