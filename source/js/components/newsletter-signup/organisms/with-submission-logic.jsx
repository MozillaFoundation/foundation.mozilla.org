import React from "react";
import { getText } from "../../petition/locales";

/**
 * Higher-order component that handles form submission logic and validation
 * for newsletter signup forms.
 */
function withSubmissionLogic(WrappedComponent) {
  return class extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        errors: {},
      };

      this.validators = {
        email: (value) => {
          if (!value) {
            return getText(`This is a required section.`);
          }

          const emailRegex = new RegExp(/[^@]+@[^.@]+(\.[^.@]+)+$/);
          if (!emailRegex.test(value)) {
            return getText(`Please enter a valid email address.`);
          }

          return null;
        },
        privacy: (value) => {
          if (value !== "true") {
            return getText(`Please check this box if you want to proceed.`);
          }
          return null;
        },
      };
    }

    /**
     * Validate a single field
     *
     * @param {string} name - name of the field
     * @param {string} value - value of the field
     * @returns {object} - { [name]: errorMessage }
     */
    validateField(name, value) {
      const validator = this.validators[name];

      if (!validator) return {};

      return { [name]: validator(value) };
    }

    /**
     * Validate all fields in the form and update state with the new errors
     *
     * @param {object} formData - { [name]: value } pairs
     * @param {function} done - callback function
     * @returns {void}
     */
    validateForm(formData, done) {
      // validate all fields
      // and combine { [name] : errorMessage } pairs into a single object
      const newErrors = Object.entries(formData)
        .map(([name, value]) => {
          return this.validateField(name, value);
        })
        .reduce((acc, curr) => {
          return { ...acc, ...curr };
        }, {});

      // update state with new errors
      this.setState({ errors: newErrors }, () => {
        done();
      });
    }

    /**
     * Form submission handler
     *
     * @param {object} event - event object
     * @param {object} formData - { [name]: value } pairs
     * @returns {void}
     */
    handleSubmit(event, formData) {
      event.preventDefault();

      this.validateForm(formData, () => {
        // Check if there's any error messages in this.state.errors object
        // if there's none, we can submit the form
        if (Object.values(this.state.errors).every((error) => !error)) {
          console.log("-[NO ERRORS. CAN SUBMIT FORM NOW]-");
          // [TODO] form submission logic goes here (will be tackled in a separate PR)
        }
      });
    }

    /**
     * Render the wrapped component with additional props
     */
    render() {
      return (
        <WrappedComponent
          {...this.props}
          noBrowserValidation={true}
          errors={this.state.errors}
          onSubmit={(event, formData) => this.handleSubmit(event, formData)}
        />
      );
    }
  };
}

export default withSubmissionLogic;
