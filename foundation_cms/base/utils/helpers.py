import json
from pathlib import Path

from django.core.files.images import ImageFile
from wagtail.blocks.stream_block import StreamValue
from wagtail.images import get_image_model

Image = get_image_model()


def import_image_from_manifest(manifest, key, image_dir):
    """
    Given a key from the image manifest, import the corresponding image file
    and create or reuse a Wagtail Image object. Returns a dict with ID and alt text.
    """
    entry = manifest.get(key)
    if not entry:
        raise ValueError(f"Missing image key in manifest: '{key}'")

    file_path = image_dir / entry["filename"]
    if not file_path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    with open(file_path, "rb") as f:
        django_file = ImageFile(f, name=entry["filename"])

        # Check if image already exists
        existing = Image.objects.filter(title=entry["alt_text"], file=f"original_images/{entry['filename']}").first()
        if existing:
            return {"id": existing.id, "alt_text": entry["alt_text"]}

        # Create new image
        image = Image.objects.create(title=entry["alt_text"], file=django_file)
        return {"id": image.id, "alt_text": entry["alt_text"]}


def inject_images_into_data(data, manifest, image_dir):
    """
    Recursively walk JSON data and replace any "image" or "thumbnail" keys
    that reference a manifest key with a real image ID (int).
    Also supports nested CustomImageBlock-like dicts.
    """
    if isinstance(data, dict):
        updated = {}
        for key, value in data.items():
            if key in ["image", "thumbnail"]:
                # Case 1: "image": "hero_thumb"
                if isinstance(value, str) and value in manifest:
                    image_info = import_image_from_manifest(manifest, value, image_dir)
                    updated[key] = image_info["id"]

                # Case 2: "image": { "image": "hero_thumb", ... }
                elif isinstance(value, dict) and isinstance(value.get("image"), str):
                    image_info = import_image_from_manifest(manifest, value["image"], image_dir)
                    updated[key] = {
                        **value,
                        "image": image_info["id"],
                        "alt_text": image_info.get("alt_text", value.get("alt_text", "")),
                    }

                else:
                    # Nested dict case
                    updated[key] = inject_images_into_data(value, manifest, image_dir)

            else:
                updated[key] = inject_images_into_data(value, manifest, image_dir)

        return updated

    elif isinstance(data, list):
        return [inject_images_into_data(item, manifest, image_dir) for item in data]

    return data


def load_manifest_with_partials(manifest_path: Path) -> dict:
    """
    Loads a manifest and expands filename values (ending in .json).
    Special handling for StreamField lists nested under keys like 'body'.
    """
    base_dir = manifest_path.parent

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    def resolve(value):
        if isinstance(value, str) and value.endswith(".html"):
            # Load plain HTML file as a string
            return (base_dir / value).read_text(encoding="utf-8")

        if isinstance(value, str) and value.endswith(".json"):
            with open(base_dir / value, "r", encoding="utf-8") as f:
                resolved_value = json.load(f)

                # Join lists of strings (e.g. rich text fragments)
                if isinstance(resolved_value, list) and all(isinstance(item, str) for item in resolved_value):
                    return "".join(resolved_value)

                return resolved_value

        elif isinstance(value, list):
            # New: each item must be {type, value}
            result = []
            for item in value:
                if isinstance(item, dict) and "type" in item and "value" in item:
                    resolved_value = resolve(item["value"])
                    result.append({"type": item["type"], "value": resolved_value})
                else:
                    result.append(resolve(item))
            return result

        elif isinstance(value, dict):
            if all(isinstance(v, str) and v.endswith((".json", ".html")) for v in value.values()):
                return [{"type": block_type, "value": resolve(filename)} for block_type, filename in value.items()]
            else:
                return {k: resolve(v) for k, v in value.items()}

        elif isinstance(value, list):
            resolved = [resolve(v) for v in value]
            if all(isinstance(item, str) for item in resolved):
                return "".join(resolved)
            return resolved

        return value

    return {k: resolve(v) for k, v in manifest.items()}


def to_streamfield_value(raw_data, stream_block):
    """
    Converts raw JSON into a Wagtail StreamField value, preserving block structure.
    """
    return StreamValue(stream_block, raw_data, is_lazy=True)
