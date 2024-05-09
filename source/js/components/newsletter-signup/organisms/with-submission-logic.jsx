import React from "react";
import PropTypes from "prop-types";
import { ReactGA } from "../../../common";

/**
 * Higher-order component that handles form submission logic and validation
 * for newsletter signup forms.
 */
function withSubmissionLogic(WrappedComponent) {
  class WithSubmissionLogicComponent extends React.Component {
    constructor(props) {
      super(props);

      this.API_SUBMISSION_STATUS = {
        NONE: "none", // no submission has been made yet
        PENDING: "pending", // a call has been initiated but response has not been received yet
        SUCCESS: "success", // response has been received and status code is 201
        ERROR: "error", // response has been received but status code is not 201
      };

      this.state = {
        apiSubmissionStatus: this.API_SUBMISSION_STATUS.NONE,
        errors: {},
      };

      this.validators = {
        email: (value) => {
          if (!value) {
            return gettext("This is a required section.");
          }

          // Regex copied from join.jsx
          const emailRegex = new RegExp(/[^@]+@[^.@]+(\.[^.@]+)+$/);
          if (!emailRegex.test(value)) {
            return gettext("Please enter a valid email address.");
          }

          return null;
        },
        privacy: (value) => {
          if (value !== "true") {
            return gettext("Please check this box if you want to proceed.");
          }
          return null;
        },
      };
    }

    /**
     * Ensure that the parent component is informed
     * about this component being mounted (primarily
     * used in the context of automated testing)
     */
    componentDidMount() {
      if (this.props.whenLoaded) {
        this.props.whenLoaded();
      }
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
     * Track form submission with GA and GTM
     *
     * @param {object} formData - { [name]: value } pairs
     * @returns {void}
     */
    trackFormSubmit(formData) {
      ReactGA.event({
        category: `signup`,
        action: `form submit tap`,
        label: `Signup submitted from ${
          this.props.formPosition ? this.props.formPosition : document.title
        }`,
      });

      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: "form_submission",
        form_type: "newsletter_signup",
        form_location: this.props.formPosition || null,
        country: formData.country,
        language: formData.language,
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

      this.trackFormSubmit(formData);

      this.validateForm(formData, () => {
        // Check if there's any error messages in this.state.errors object
        // if there's none, we can submit the form
        if (Object.values(this.state.errors).every((error) => !error)) {
          this.submitDataToApi(formData)
            .then(() => {
              this.setState({
                apiSubmissionStatus: this.API_SUBMISSION_STATUS.SUCCESS,
              });
              this.props.handleSubmissionSuccess?.(true);
            })
            .catch(() => {
              // [TODO][FIXME] We need to let the user know that something went wrong
              // https://github.com/MozillaFoundation/foundation.mozilla.org/issues/11406
              this.setState({
                apiSubmissionStatus: this.API_SUBMISSION_STATUS.ERROR,
              });
            });
        }
      });
    }

    /**
     *  Submit data to API
     *
     * @param {*} formData  - { [name]: value } pairs
     * @returns {Promise} - resolves if response status is 201, rejects otherwise
     */
    async submitDataToApi(formData) {
      this.setState({
        apiSubmissionStatus: this.API_SUBMISSION_STATUS.PENDING,
      });

      let payload = {
        givenNames: formData.firstName,
        surname: formData.lastName,
        email: formData.email,
        country: formData.country,
        lang: formData.language,
        // keeping query params in source url for newsletter signups:
        // https://github.com/mozilla/foundation.mozilla.org/issues/4102#issuecomment-590973606
        source: window.location.href,
      };

      try {
        const res = await fetch(this.props.apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify(payload),
          timeout: 5000,
        });

        if (res.status !== 201) {
          this.setState({
            apiError: gettext(
              "Something went wrong and your signup wasn't completed. Please try again later."
            ),
          });
          throw new Error(res.statusText);
        }
      } catch (error) {
        this.setState({
          apiError: gettext(
            "Something went wrong and your signup wasn't completed. Please try again later."
          ),
        });
        throw error;
      }
    }

    /**
     * Generate the CTA header message for different scenarios
     *
     * @param {string} ctaHeader - default CTA header message
     * @returns {string} - CTA header message
     */
    generateCtaHeader(ctaHeader) {
      let message = ctaHeader;

      if (
        this.state.apiSubmissionStatus === this.API_SUBMISSION_STATUS.SUCCESS
      ) {
        message = gettext("Thanks!");
      }

      return message;
    }

    /**
     * Generate the CTA description message for different scenarios
     *
     * @param {*} ctaDescription - default CTA description message
     * @returns {string} - CTA description message
     */
    generateCtaDescription(ctaDescription) {
      let message = ctaDescription;

      if (
        this.state.apiSubmissionStatus === this.API_SUBMISSION_STATUS.SUCCESS
      ) {
        message = (
          <>
            <p>
              {pgettext(
                "Pre-bold text of: If you haven’t previously confirmed your opt-in to a Mozilla-related email subscription you may have to do so now. <strong>Please check your inbox or spam filter for an email from us to click and confirm your subscription</strong>.",
                "If you haven’t previously confirmed your opt-in to a Mozilla-related email subscription you may have to do so now. "
              )}
              <strong>
                {pgettext(
                  "Bold text of: If you haven’t previously confirmed your opt-in to a Mozilla-related email subscription you may have to do so now. <strong>Please check your inbox or spam filter for an email from us to click and confirm your subscription</strong>.",
                  "Please check your inbox or spam filter for an email from us to click and confirm your subscription"
                )}
              </strong>
              {pgettext(
                "If you haven’t previously confirmed your opt-in to a Mozilla-related email subscription you may have to do so now. <strong>Please check your inbox or spam filter for an email from us to click and confirm your subscription</strong>.",
                "."
              )}
            </p>
            <p>
              {pgettext(
                "Pre-link text of: If you have already confirmed your opt-in to receive Mozilla-related emails, you can now <a href='https://www.mozilla.org/newsletter/recovery/' target='_blank'>manage your subscriptions</a> and update your email preferences.",
                "If you have already confirmed your opt-in to receive Mozilla-related emails, you can now "
              )}
              <a
                href="https://www.mozilla.org/newsletter/recovery/"
                target="_blank"
              >
                {pgettext(
                  "Link text of: If you have already confirmed your opt-in to receive Mozilla-related emails, you can now <a href='https://www.mozilla.org/newsletter/recovery/' target='_blank'>manage your subscriptions</a> and update your email preferences.",
                  "manage your subscriptions"
                )}
              </a>
              {pgettext(
                "Post-link text of: If you have already confirmed your opt-in to receive Mozilla-related emails, you can now <a href='https://www.mozilla.org/newsletter/recovery/' target='_blank'>manage your subscriptions</a> and update your email preferences.",
                " and update your email preferences."
              )}
            </p>
          </>
        );
      }

      return message;
    }

    /**
     * Render the wrapped component with additional props
     */
    render() {
      let { forwardedRef, ctaHeader, ctaDescription, ...otherProps } =
        this.props;

      return (
        <WrappedComponent
          {...otherProps}
          ref={forwardedRef}
          noBrowserValidation={true}
          errors={this.state.errors}
          apiError={this.state.apiError}
          onSubmit={(event, formData) => this.handleSubmit(event, formData)}
          ctaHeader={this.generateCtaHeader(ctaHeader)}
          ctaDescription={this.generateCtaDescription(ctaDescription)}
          hideForm={
            this.state.apiSubmissionStatus ===
            (this.API_SUBMISSION_STATUS.SUCCESS ||
              this.API_SUBMISSION_STATUS.ERROR)
          }
          apiSubmissionStatus={this.state.apiSubmissionStatus}
        />
      );
    }
  }

  WithSubmissionLogicComponent.propTypes = {
    apiUrl: PropTypes.string.isRequired,
    ctaHeader: PropTypes.string.isRequired,
    ctaDescription: PropTypes.oneOfType([PropTypes.string, PropTypes.node])
      .isRequired,
    formPosition: PropTypes.string,
    whenLoaded: PropTypes.func,
  };

  return React.forwardRef((props, ref) => {
    return <WithSubmissionLogicComponent {...props} forwardedRef={ref} />;
  });
}

export default withSubmissionLogic;
