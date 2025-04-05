export const IS_STATIC_BUILD =
  import.meta && import.meta.env && import.meta.env.MODE === "production";

// Function to display a generic fetching message
export function createFetchingMessage(name) {
  const div = document.createElement("div");
  div.textContent = `🔄 Fetching ${name} from Django Pattern Library...`;
  return div;
}

// Function to load a static component file in build mode
export async function loadStaticComponent(path, wrapper) {
  try {
    const response = await fetch(path);
    const html = await response.text();
    wrapper.innerHTML = html;
  } catch (error) {
    console.error(`❌ Error loading static component ${path}:`, error);
    wrapper.innerHTML = `<div>Error loading component</div>`;
  }
}

// Function to dynamically fetch components in development mode
export async function fetchDjangoComponent(url, wrapper) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to load component: ${response.statusText}`);
    }
    const text = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(text, "text/html");
    let component = doc.body.firstElementChild;

    if (!component) {
      throw new Error("No valid component found.");
    }

    // Replace placeholder once fetched
    wrapper.replaceChildren(component);
  } catch (error) {
    console.error(`❌ Error fetching component: ${error.message}`);
    wrapper.textContent = `Error loading component: ${error.message}`;
  }
}

// Generic function for creating Storybook stories that work in both dev & build mode
export function createStory(name, url, staticPath) {
  const wrapper = document.createElement("div");

  if (IS_STATIC_BUILD) {
    console.log(`Loading pre-fetched static ${name} component.`);
    loadStaticComponent(staticPath, wrapper);
    return wrapper;
  }

  console.log(`Fetching ${name} component dynamically from Django...`);
  wrapper.appendChild(createFetchingMessage(name));

  fetchDjangoComponent(url, wrapper);

  return wrapper;
}
