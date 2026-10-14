// LP inputs/dropdown behavior, with form values and keyboard navigation.
export default function initDropdown(root, choices, id) {
  const trigger = root.querySelector(".mzf-c-dropdown__trigger");
  const menu = root.querySelector(".mzf-c-dropdown__menu");
  const value = root.querySelector(".mzf-c-dropdown__value");
  const input = root.querySelector("input");
  menu.id = id;
  value.id = `${id}-value`;
  trigger.setAttribute("aria-controls", id);
  const options = choices.map((choice) => {
    const option = document.createElement("li");
    option.className = "mzf-c-dropdown__option";
    option.setAttribute("role", "option");
    option.setAttribute("aria-selected", "false");
    option.tabIndex = -1;
    option.textContent = choice.label;
    option.dataset.value = choice.value;
    return option;
  });
  menu.replaceChildren(...options);
  let frame;
  let timer;
  let search = "";
  let lastKeyTime = 0;

  const isOpen = () => trigger.getAttribute("aria-expanded") === "true";
  const reducedMotion = () =>
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function close(focusTrigger = false, immediate = false) {
    cancelAnimationFrame(frame);
    clearTimeout(timer);
    trigger.setAttribute("aria-expanded", "false");
    root.classList.remove("mzf-c-dropdown--open");
    const finish = () => {
      menu.hidden = true;
      root.classList.remove("mzf-c-dropdown--closing");
    };
    if (immediate || reducedMotion()) finish();
    else {
      root.classList.add("mzf-c-dropdown--closing");
      const duration =
        parseFloat(
          getComputedStyle(root).getPropertyValue(
            "--mzf-dropdown-close-duration",
          ),
        ) || 150;
      timer = setTimeout(finish, duration);
    }
    if (focusTrigger) trigger.focus();
  }

  function open() {
    clearTimeout(timer);
    cancelAnimationFrame(frame);
    menu.hidden = false;
    root.classList.remove("mzf-c-dropdown--closing");
    // The production country list is longer than the reference's sample list.
    // Keep every option reachable within the available viewport.
    const rect = trigger.getBoundingClientRect();
    const gap =
      parseFloat(getComputedStyle(menu).insetBlockStart) - rect.height || 6;
    menu.style.maxBlockSize = `${Math.max(0, window.innerHeight - rect.bottom - gap)}px`;
    menu.style.overflowY = "auto";
    const show = () => {
      root.classList.add("mzf-c-dropdown--open");
      trigger.setAttribute("aria-expanded", "true");
    };
    if (reducedMotion()) show();
    else frame = requestAnimationFrame(show);
    menu.focus();
  }

  function choose(option) {
    input.value = option.dataset.value;
    value.textContent = option.textContent;
    trigger.setAttribute("aria-describedby", value.id);
    value.classList.remove("mzf-c-dropdown__value--placeholder");
    options.forEach((item) =>
      item.setAttribute("aria-selected", String(item === option)),
    );
    input.dispatchEvent(new Event("change", { bubbles: true }));
    close(true);
  }

  trigger.addEventListener("click", () => {
    if (isOpen()) close();
    else open();
  });
  trigger.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      open();
      const selected = options.find(
        (option) => option.getAttribute("aria-selected") === "true",
      );
      (
        selected || (event.key === "ArrowUp" ? options.at(-1) : options[0])
      )?.focus();
    }
  });
  menu.addEventListener("click", (event) => {
    const option = event.target.closest(".mzf-c-dropdown__option");
    if (option) choose(option);
  });
  menu.addEventListener("keydown", (event) => {
    let index = options.indexOf(document.activeElement);
    if (event.key === "Escape") {
      event.preventDefault();
      close(true);
      return;
    }
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (index >= 0) choose(options[index]);
      return;
    }
    if (event.key === "ArrowDown") index = (index + 1) % options.length;
    else if (event.key === "ArrowUp")
      index = (index < 0 ? options.length : index) - 1;
    else if (event.key === "Home") index = 0;
    else if (event.key === "End") index = options.length - 1;
    else if (
      event.key.length === 1 &&
      !event.ctrlKey &&
      !event.metaKey &&
      !event.altKey
    ) {
      const now = Date.now();
      search = now - lastKeyTime > 700 ? event.key : search + event.key;
      lastKeyTime = now;
      index = options.findIndex((option) =>
        option.textContent
          .toLocaleLowerCase()
          .startsWith(search.toLocaleLowerCase()),
      );
    } else return;
    event.preventDefault();
    options[index]?.focus();
  });
  root.addEventListener("focusout", (event) => {
    if (!root.contains(event.relatedTarget)) close(false, true);
  });
  document.addEventListener("click", (event) => {
    if (!root.contains(event.target) && !menu.hidden) close();
  });
  return { close };
}
