const MOBILE = 'iphone-6';
const DESKTOP = 'macbook-13';
const viewports = [MOBILE, DESKTOP]

const A11Y_CONFIG = {
  reporter: "v2"
}

const EXCLUDE_CONSTANTS = [
  ['.join-us'], // Signups
  ['.wide-screen-menu', '.nav-links'], // Desktop Nav
  ['.narrow-screen-menu-container', '.nav-links'], //Mobile Nav
  ['.donate-banner *'] // Donate Banner
  ['.site-footer', '#language-switcher'], // Language Switcher
  ['.site-footer a.logo'] // Footer Logo
]

const EXCLUDE_PNI_CONSTANTS = EXCLUDE_CONSTANTS.concat([
    ['#coral-talk-stream', 'iframe'] // Commenting
  ])

export { viewports, MOBILE, DESKTOP, A11Y_CONFIG, EXCLUDE_CONSTANTS, EXCLUDE_PNI_CONSTANTS }
