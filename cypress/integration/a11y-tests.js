const customViolationLogger = violation => cy.task("log", violation)
const customViolationHandler = violation => cy.task("log", violation)

const A11Y_CONFIG = {
  branding: {
    brand: "Mozilla",
    application: "FoMo"
  },
  reporter: "v2",
  checks: [
    {
      id: testCheck
    }
  ],
  rules: [
    {
      id: testRules
    }
  ]
}

describe(`A11y Tests`, () => {
  beforeEach(() => {
    cy.injectAxe();
    cy.configureAxe(A11Y_CONFIG);
  });

  before(() => {
    cy.visit(`/`);
    cy.window()
      .its(`main-js:react:finished`)
      .should(`equal`, true);
    cy.wait(500);
  });

  it(`Homepage`, () => {
    cy.checkA11y(
      document,
      {
        runOnly: ['wcag2aa', 'section508', 'best-practice'],
        logger: customViolationLogger,
        asserter: customViolationHandler
      },
      (err, results) => {
        if (err) throw err;
        console.log(`Results: ${results}`);
      }
    )
  });
});
