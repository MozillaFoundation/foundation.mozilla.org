/**
 * This module defines styles for different newsletter forms. It should contain solely style definitions and not any logic.
 * Each key in the STYLES object corresponds to a "data-form-style" attribute value on <div class="newsletter-signup-module" ..> (like "blog-body" or "footer")
 *
 * @module form-specific-style
 *
 * @property {buttonPosition} STYLES.x.buttonPosition
 *    - The button position for the form based on style guide. Possible values are "side" and "bottom".
 * @property {buttonStyle} STYLES.x.buttonStyle
 *    - The button style for the form based on style guide. Possible values are "primary" and "secondary".
 * @property {buttonWidthClasses} STYLES.x.buttonWidthClasses
 *    - CSS classes for the button width. e.g., tw-w-full, tw-w-auto
 * @property {string} STYLES.x.fieldStyle
 *    - The style type for the form field based on Figma's design system. Possible values are "filled" and "outlined".
 * @property {string} STYLES.x.formContainerClass
 *    - CSS classes for the <div> that wraps around the actual <form> element.
 * @property {number} STYLES.x.headingLevel
 *    - The heading level for heading element.
 * @property {string} STYLES.x.headingClass
 *    - CSS classes for the heading element.
 * @property {string} STYLES.x.descriptionClass
 *    - CSS classes for the description element.
 * @property {string} STYLES.x.innerWrapperClass
 *    - CSS classes for the inner wrapper of the form.
 * @property {string} STYLES.x.introContainerClass
 *    - CSS classes for the <div> that wraps around the intro text.
 */

export const FORM_STYLE = {
  "blog-body": {
    fieldStyle: "outlined",
    headingLevel: 2,
    headingClass: `tw-h3-heading`,
    innerWrapperClass: `
      tw-relative tw-border tw-px-8 tw-pt-14 tw-pb-12 medium:tw-p-16
      before:tw-absolute before:tw-top-0 before:tw-left-1/2 before:-tw-translate-x-1/2 before:-tw-translate-y-1/2 before:tw-content-[''] before:tw-inline-block before:tw-w-[72px] before:tw-h-14 before:tw-bg-[url('../_images/glyphs/letter.svg')] before:tw-bg-white before:tw-bg-no-repeat before:tw-bg-center before:tw-bg-[length:24px_auto]
    `,
  },
  "callout-box": {
    fieldStyle: "filled",
    headingLevel: 3,
    headingClass: `tw-h3-heading medium:tw-w-4/5`,
    descriptionClass: `medium:tw-w-4/5`,
  },
  "callout-box:2-col": {
    buttonPosition: "bottom",
    buttonStyle: "secondary",
    buttonWidthClasses: "tw-w-auto",
    fieldStyle: "outlined",
    formContainerClass: "tw-flex-col tw-w-1/2 large:tw-pl-24 tw-mt-8",
    headingLevel: 3,
    headingClass: "tw-h1-heading",
    innerWrapperClass: "tw-flex tw-gap-8",
    introContainerClass: "tw-flex-col tw-w-1/2 large:tw-pr-24",
  },
  footer: {
    fieldStyle: "outlined",
    headingLevel: 4,
    headingClass: `tw-h5-heading`,
  },
  "home-body": {
    buttonPosition: "bottom",
    buttonStyle: "primary",
    buttonWidthClasses: "tw-w-full",
    fieldStyle: "outlined",
    headingLevel: 3,
    headingClass: "tw-h5-heading",
  },
};
