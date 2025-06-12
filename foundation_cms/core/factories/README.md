# Modular Wagtail Page Loading System

This repository uses a manifest-driven architecture to define and load Wagtail pages using structured JSON, HTML, and image manifests. It is designed for modularity, maintainability, and team collaboration across developers of all levels.

## Overview

This system enables:

- Modular JSON definitions for Wagtail `Page` content
- Partial includes per StreamField block
- Optional `.html` files for rich text content
- Declarative image manifests to upload and associate images
- Validation of StreamField structure before save
- Automatic content injection using factories and management commands

## Directory Structure

Each page type (e.g. homepage, event page) lives in its own subfolder within `factories/data/`.

```
factories/
├── data/
│ └── homepage/
│ ├── manifest.json
│ ├── image_manifest.json
│ ├── hero_accordion.json
│ ├── body/
│ │ ├── tabbed_content.json
│ │ ├── rich_text.html
│ └── images/
│ ├── hero.jpg
│ ├── mozfest.jpg
│ ├── community.jpg
```

## `manifest.json`

This file defines the structure of the page. It references content **partials** and provides the top-level page configuration.

```json
{
  "title": "Redesign Homepage",
  "slug": "redesign-home",
  "hero_accordion": "hero_accordion.json",
  "body": [
    { "type": "portait_card_set_bock", "value": "body/portrait_card_set.json" },
    { "type": "rich_text", "value": "body/rich_text.html" },
    { "type": "tabbed_content", "value": "body/tabbed_content.json" },
    { "type": "rich_text", "value": "body/cta.html" }
  ]
}
```

## How Partials Work

Each file referenced in `manifest.json` is treated as a partial and resolved at runtime using the `load_manifest_with_partials()` helper.

- If the value is a `.json` file, it is parsed as structured data (e.g. tab block content, image block dictionaries).
- If the value is a `.html` file, it is loaded as a plain string and used as rich text.
- If the value is a list of strings, it is automatically joined into a single HTML fragment.

This allows complex pages to be composed from modular, reusable pieces.

### Example Manifest Snippet

```json
{
  "type": "rich_text",
  "value": "body/intro.html"
}
```

This tells the loader to:

1. Open the file `body/intro.html`
2. Read its contents as a raw string
3. Use that string as the value for a `rich_text` StreamField block

Note: The `type` key must be available and match the StreamField block's `key` or you'll get a key error.

### Example Partial: `body/intro.html`

```html
<h2>Welcome to Our Site</h2>
<p>This content was loaded from a partial HTML file.</p>
```

## Supported Formats

- `.json`: for structured data such as tabbed blocks or StreamField lists
- `.html`: for raw rich text content (plain strings)

## `image_manifest.json`

This file defines image keys, the corresponding files, and alt text for accessibility.

```json
{
  "hero_accordion__1": {
    "filename": "hero_accordion__2.jpg",
    "alt_text": "A visual opening"
  },
  "hero_accordion__2": {
    "filename": "hero_accordion__2.jpg",
    "alt_text": "Another image"
  },
  "tabbed_content__tab_1": {
    "filename": "placeholder__1.jpg",
    "alt_text": "Some relavent alt text"
  },
  "tabbed_content__tab_2": {
    "filename": "placeholder__2.jpg",
    "alt_text": "Other relavent alt text"
  }
}
```
These keys are referenced in content JSON as:

```
"image": "tabbed_content__card_image"
```

and automatically resolved to the correct uploaded image ID. 

## Factory Helper Functions

The following helper functions support this system and are available in `foundation_cms/base/utils/helpers.py`.

### `load_manifest_with_partials(path: Path) -> dict`

- Recursively loads JSON or HTML partials referenced in a manifest
- Supports block lists or named block mappings
- Joins HTML fragments or arrays of strings automatically

### `inject_images_into_data(data, manifest, image_dir)`

- Replaces `"image": "key"` with image IDs based on the manifest
- Uploads images if they don't already exist
- Works with model fields and nested StreamField blocks

### `to_streamfield_value(raw_data, stream_block)`

- Converts JSON-formatted block data into a native `StreamValue`
- Used to assign data to a `StreamField` before saving

## Workflow for Adding a New Page Type

1. Create a folder in `factories/data/` with the desired name.
2. Create a `manifest.json` file and any needed partials into the root or subfolders (e.g. `body/`).
3. Define an `image_manifest.json` and place all image files under `images/`.
4. Reference this folder and manifest path in your factory code.
5. Use the `load_redesign_data.py` pattern to run factory code inject, validate, and publish the page.

## Development Tips

- Use `.html` files for rich text for easier editing and cleaner diffs
- Keep image keys namespaced (e.g. `tabbed_content__card_image`) for clarity
- Validate content structure before loading with `validate_streamfield_blocks()`
- Join multiple HTML fragments via arrays or `.html` partials

## Example Command to Load Data

- This is the command to load in redesign data it does the following:

1. Checks if the homepage already exists and if there's a --force flag. Will delete and continue to create new if so. Great for rapid destruction and creation.
2. Create the homepage from json
3. Devs will add other page factories here.
4. Create the wagtail site, and assign the homepage to the root.

```
python manage.py load_redesign_data --force
```