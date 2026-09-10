import { ensureCsrfToken } from "../utils/csrf.js";

export function initLanguageSwitcher(root = document) {
  const form = root.getElementById("language-switcher-form");
  const selector = root.getElementById("language-switcher");
  const nextInput = root.getElementById("language-next");
  const tokenInput = root.getElementById("language-csrftoken");

  if (!form || !selector || !nextInput || !tokenInput) return;

  selector.addEventListener("change", async () => {
    const option = selector.options[selector.selectedIndex];
    nextInput.value = option.dataset.url || "/";
    tokenInput.value = await ensureCsrfToken();
    form.submit();
  });
}
