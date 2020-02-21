import {
  viewports,
  A11Y_CONFIG,
  EXCLUDE_PNI_CONSTANTS
} from "./global_variables";

let dimension;

const PNI_A11Y = () => {
  viewports.forEach(viewport => {
    if (viewport === "iphone-5") {
      dimension = "Mobile";
    } else {
      dimension = "Desktop";
    }

    context(`${dimension} Assessments`, () => {
      it.skip("PNI homepage Accessibility ", () => {
        cy.viewport(viewport);
        cy.visit("en/privacynotincluded/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });

      it.skip("PNI Category Page", () => {
        cy.viewport(viewport);
        cy.visit("/en/privacynotincluded/categories/toys-games/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });

      it.skip("PNI Product Page ", () => {
        cy.viewport(viewport);
        cy.visit("/en/privacynotincluded/products/percy-cypress/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });

      it.skip("PNI About Page ", () => {
        cy.viewport(viewport);
        cy.visit("/en/privacynotincluded/about/");
        cy.window()
          .its(`bg-main-js:react:finished`)
          .should(`equal`, true);
        cy.wait(500);
        cy.injectAxe()
          .configureAxe(A11Y_CONFIG)
          .checkA11y({ exclude: EXCLUDE_PNI_CONSTANTS });
      });
    });
  });
};

export default PNI_A11Y;
