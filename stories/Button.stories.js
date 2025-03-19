const PATTERN_LIBRARY_URL =
  "http://localhost:8000/pattern-library/render-pattern/patterns/buttons/primary.html";

export default {
  title: "Button",
  tags: ["autodocs"],
};

export const Primary = () => {
  // Storybook requires a DOM node to be returned immediately, but fetching from Django is asynchronous.
  // We first return a placeholder div ("Fetching ...") so Storybook has something to render.

  const loadingDiv = document.createElement("div");
  loadingDiv.textContent = "Fetching component from Django Pattern Library...";

  (async () => {
    try {
      const response = await fetch(PATTERN_LIBRARY_URL);

      if (!response.ok) {
        throw new Error(
          `Failed to load component: ${response.status} ${response.statusText}`
        );
      }

      const sourcePageHtml = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(sourcePageHtml, "text/html");

      let button = doc.querySelector("button");

      if (!button) {
        throw new Error("No <button> tag found in the fetched HTML.");
      }

      loadingDiv.replaceWith(button);
    } catch (error) {
      console.error("Error loading component:", error);
      loadingDiv.textContent = `Error: ${error.message}`;
    }
  })();

  return loadingDiv;
};
