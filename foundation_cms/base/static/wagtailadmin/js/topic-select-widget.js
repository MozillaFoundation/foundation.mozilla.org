/**
 * TopicSelectWidget — tag-picker behaviour for ClusterTaggableManager fields.
 *
 * Initialises every .ts-widget on the page:
 *  - click the bar → open the dropdown
 *  - type to filter options
 *  - click an option → add a chip, hide the option
 *  - click ✕ on a chip → remove it, restore the option
 *  - Backspace on empty input → remove last chip
 *  - click outside → close dropdown
 */

function initTopicSelectWidget(widget) {
  const hidden = widget.querySelector("input[type=hidden]");
  const bar = widget.querySelector(".ts-bar");
  const input = widget.querySelector(".ts-input");
  const dropdown = widget.querySelector(".ts-dropdown");

  function getSelectedValues() {
    return [...bar.querySelectorAll(".ts-chip")].map((chip) => chip.dataset.value);
  }

  function syncHiddenInput() {
    const selected = getSelectedValues();
    hidden.value = selected.map((v) => (v.includes(",") ? `"${v}"` : v)).join(", ");
    input.placeholder = selected.length ? "" : "Select topics…";
  }

  function wireChipRemove(chip) {
    chip.querySelector("button").addEventListener("click", (e) => {
      e.stopPropagation();
      const value = chip.dataset.value;
      chip.remove();
      const option = dropdown.querySelector(`.ts-option[data-value="${value}"]`);
      if (option) option.hidden = false;
      syncHiddenInput();
    });
  }

  function addChip(value) {
    const chip = document.createElement("span");
    chip.className = "ts-chip";
    chip.dataset.value = value;
    chip.innerHTML = `${value}<button type="button" aria-label="Remove ${value}">&times;</button>`;
    wireChipRemove(chip);
    bar.insertBefore(chip, input);
    const option = dropdown.querySelector(`.ts-option[data-value="${value}"]`);
    if (option) option.hidden = true;
    syncHiddenInput();
  }

  function openDropdown() {
    dropdown.style.display = "block";
  }

  function closeDropdown() {
    dropdown.style.display = "none";
  }

  // Wire up server-rendered chips
  bar.querySelectorAll(".ts-chip").forEach(wireChipRemove);

  bar.addEventListener("click", () => {
    openDropdown();
    input.focus();
  });

  input.addEventListener("input", function () {
    const filter = this.value.toLowerCase();
    const selected = getSelectedValues();
    dropdown.querySelectorAll(".ts-option").forEach((option) => {
      if (selected.includes(option.dataset.value)) {
        option.hidden = true;
        return;
      }
      option.hidden = !option.textContent.toLowerCase().includes(filter);
    });
    openDropdown();
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") e.preventDefault();
    if (e.key === "Backspace" && !this.value) {
      const chips = bar.querySelectorAll(".ts-chip");
      if (chips.length) chips[chips.length - 1].querySelector("button").click();
    }
  });

  dropdown.addEventListener("click", (e) => {
    const option = e.target.closest(".ts-option");
    if (!option || option.hidden) return;
    addChip(option.dataset.value);
    input.value = "";
    input.focus();
  });

  document.addEventListener("mousedown", (e) => {
    if (!widget.contains(e.target)) closeDropdown();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".ts-widget").forEach(initTopicSelectWidget);
});
