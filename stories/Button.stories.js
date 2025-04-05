import { createStory } from "./utils";

export default {
  title: "Button",
};

// Centralized URLs for Django Pattern Library components
const PATTERN_LIBRARY_URLS = {
  primary:
    "http://localhost:8000/pattern-library/render-pattern/patterns/buttons/primary.html",
  secondary:
    "http://localhost:8000/pattern-library/render-pattern/patterns/buttons/secondary.html",
};

// Centralized static file paths for pre-fetched components
const STATIC_FILE_PATHS = {
  primary: "/components/primary-button.html",
  secondary: "/components/secondary-button.html",
};

// Storybook exports
export const Primary = () =>
  createStory(
    "Primary Button",
    PATTERN_LIBRARY_URLS.primary,
    STATIC_FILE_PATHS.primary
  );
export const Secondary = () =>
  createStory(
    "Secondary Button",
    PATTERN_LIBRARY_URLS.secondary,
    STATIC_FILE_PATHS.secondary
  );
