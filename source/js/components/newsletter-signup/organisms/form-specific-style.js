/**
 * This module defines styles for different newsletter forms. It should contain solely style definitions and not any logic.
 * Each key in the STYLES object corresponds to a "data-form-style" attribute value on <div class="newsletter-signup-module" ..>
 * (like "blog-body" or "footer")
 *
 * @module form-specific-style
 * @property {number} STYLES.x.headingLevel - The heading level for heading element.
 * @property {string} STYLES.x.headingClass - CSS classes for the heading element.
 * @property {string} STYLES.x.descriptionClass - CSS classes for the description element.
 * @property {string} STYLES.x.innerWrapperClass - CSS classes for the inner wrapper of the form.
 * @property {string} STYLES.x.designSystemStyle - The style type for the form based on Figma's design system. Possible values are "filled" and "outlined".
 */

export const FORM_STYLE = {
  "blog-body": {
    headingLevel: 2,
    headingClass: `tw-h3-heading`,
    innerWrapperClass: `
      tw-relative tw-border tw-px-8 tw-pt-14 tw-pb-12 medium:tw-p-16
      before:tw-absolute before:tw-top-0 before:tw-left-1/2 before:-tw-translate-x-1/2 before:-tw-translate-y-1/2 before:tw-content-[''] before:tw-inline-block before:tw-w-[72px] before:tw-h-14 before:tw-bg-[url('../_images/glyphs/letter.svg')] before:tw-bg-white before:tw-bg-no-repeat before:tw-bg-center before:tw-bg-[length:24px_auto]
    `,
    designSystemStyle: "outlined",
  },
  "callout-box": {
    headingLevel: 3,
    headingClass: `tw-h3-heading medium:tw-w-4/5`,
    descriptionClass: `medium:tw-w-4/5`,
    designSystemStyle: "filled",
  },
  footer: {
    headingLevel: 4,
    headingClass: `tw-h5-heading`,
    designSystemStyle: "outlined",
  },
};
