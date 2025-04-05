/**
 * Fetch DPL (Design Pattern Library) components and save them for Storybook.
 *
 * This script:
 * - Fetches static HTML components from local URLs (e.g., a running Django server)
 * - Extracts the relevant DOM node using jsdom
 * - Cleans and saves each component into the Storybook static directory
 * - Adds a timestamp to track when the HTML was last fetched
 *
 * Used in:  `build-storybook` script to ensure fresh component snapshots
 */

import fs from "fs";
import fetch from "node-fetch";
import { JSDOM } from "jsdom"; // Use jsdom to simulate the DOM in Node.js

const OUTPUT_DIR = "storybook-static/components"; // Where we save fetched HTML files

const COMPONENTS = [
  {
    name: "button-primary",
    url: "http://localhost:8000/pattern-library/render-pattern/patterns/buttons/primary.html",
  },
  {
    name: "button-secondary",
    url: "http://localhost:8000/pattern-library/render-pattern/patterns/buttons/secondary.html",
  },
];

// Function to format timestamp as "YYYY-MM-DD HH:mm AM/PM UTC"
function getTimestamp() {
  const now = new Date();
  const formattedDate = now.toLocaleString("en-US", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "numeric",
    minute: "2-digit",
    hour12: true, // Uses AM/PM format
    timeZone: "UTC", // UTC timezone
  });

  return formattedDate.replace(",", "").replace(/\//g, "-") + " UTC";
  // Example output: "2024-03-20 12:34 PM UTC"
}

// Function to clear all previously fetched component files
function clearOutputDirectory() {
  if (fs.existsSync(OUTPUT_DIR)) {
    fs.readdirSync(OUTPUT_DIR).forEach((file) => {
      const filePath = `${OUTPUT_DIR}/${file}`;
      fs.unlinkSync(filePath);
    });
    console.log(`🗑️  Cleared old component files in ${OUTPUT_DIR}`);
  }
}

// Function to fetch and save a single component
async function fetchAndSaveComponent({ name, url }) {
  try {
    console.log(`🔄 Fetching ${name} component from: ${url}`);
    const response = await fetch(url);
    if (!response.ok)
      throw new Error(
        `Failed to fetch ${name} component: ${response.statusText}`,
      );

    const html = await response.text();
    const dom = new JSDOM(html);
    const document = dom.window.document;
    const component = document.body.firstElementChild;

    if (!component)
      throw new Error(`No valid component found in ${name} HTML.`);

    let staticHTML = component.outerHTML.trim();
    console.log(staticHTML);
    const timestamp = getTimestamp();
    console.log(`Successfully extracted component for ${name} at ${timestamp}`);

    // Ensure output directory exists
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    // Save component with a timestamp
    const filePath = `${OUTPUT_DIR}/${name}.html`;
    fs.writeFileSync(
      filePath,
      `<!-- Last fetched on ${timestamp} -->\n${staticHTML}`,
    );
    console.log(`✅ Saved ${name} to ${filePath}`);
  } catch (error) {
    console.error(`❌ Error fetching ${name} component:`, error);
  }
}

// Function to fetch all components
async function fetchAllComponents() {
  clearOutputDirectory();
  for (const component of COMPONENTS) {
    await fetchAndSaveComponent(component);
  }
}

fetchAllComponents();
