const A11Y_OPTIONS = {
  runOnly: {
    type: 'tag',
    value: ['section508']
  }
}

// Inject axe-core  and run a11y check with some pre-made options

context('Accessibility (A11Y)', () => {
  it('Passes accessibility tests', () => {
    cy.visit('http://localhost:8000');
    cy.injectAxe();
    cy.checkA11y(A11Y_OPTIONS);
  })
})

// describe('Accessibility testing for foundation.mozilla.org', function () {

//   before(function () {
//     cy.visit('http://localhost:8000/');

//     // Inject the axe-core library
//     cy.injectAxe();
//   });

//   it('Should load the homepage', async () => {
//     cy.url().should('http://localhost:8000');
//   });

//   it('Has a valid footrer signup', async function () {
//     cy.get('form').within(() => {
//         cy.get('.join-us[data-form-position="footer"] input').should('be.visible');
  
//         cy.get('.join-us[data-form-position="footer"] select').should('be.visible');
  
//         cy.get('.join-us[data-form-position="footer"] button').should('be.visible');
//     });
  
//     // first a11y test
//     cy.checkA11y();
//   });

//   it('Should display an thank you message after success.', async function () {
//     cy.get('.join-us[data-form-position="footer"] input').type('test@test.com');

//     cy.get('button').click();

//     // wait for the server to respond, then test for the error
//     cy.wait(1000)
//         .get('div.signup-success')
//         .should('be.visible');
//   });
// });
