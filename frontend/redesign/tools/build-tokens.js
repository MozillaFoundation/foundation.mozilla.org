/**
 * Flattens a token JSON object into a single-level map of hyphenated names to
 * raw values. Skips any key starting with "$" ($description, $meta) since
 * those are annotations, not tokens.
 *
 * A node is a leaf token once it has both "value" and "description" keys —
 * anything else is a deeper category to keep recursing into. This matches
 * the shape of the token JSON files LP passed us (see tokens/*.json), which
 * follow the W3C design token format: every leaf is a { value, description }
 * object, and references between tokens use "{dot.path}" braces.
 *
 * Example: { color: { border: { default: { value: "#161616", description: "..." } } } }
 * becomes { "color-border-default": "#161616" }
 */
function flatten(node, prefix, out) {
  for (const [key, value] of Object.entries(node)) {
    if (key.startsWith("$")) continue;

    const nextPrefix = prefix ? `${prefix}-${key}` : key;

    if (value && typeof value === "object" && "value" in value) {
      out[nextPrefix] = value.value;
    } else if (value && typeof value === "object") {
      flatten(value, nextPrefix, out);
    }
  }
  return out;
}

/**
 * Resolves "{dot.path}" references between tokens in place, e.g.
 * "color-border-default": "{color.gray.1000}" becomes "color-border-default": "#161616".
 *
 * The dot.path inside the braces is LP's original naming (matches the JSON
 * structure before flattening), so it gets converted to our hyphenated key
 * format before the lookup. Follows chained references (a token pointing at
 * a token that is itself a reference) and throws on a circular one instead
 * of infinite-looping.
 */
function resolveRefs(tokens) {
  const refPattern = /^\{(.+)\}$/;

  function resolve(value, seen) {
    const match = typeof value === "string" && value.match(refPattern);
    if (!match) return value;

    const refKey = match[1].replace(/\./g, "-");
    if (seen.has(refKey)) {
      throw new Error(`Circular token reference: ${[...seen, refKey].join(" -> ")}`);
    }
    if (!(refKey in tokens)) {
      throw new Error(`Unresolved token reference: {${match[1]}}`);
    }

    return resolve(tokens[refKey], new Set(seen).add(refKey));
  }

  for (const key of Object.keys(tokens)) {
    tokens[key] = resolve(tokens[key], new Set());
  }
  return tokens;
}
