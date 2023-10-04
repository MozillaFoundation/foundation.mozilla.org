import React, { Component } from "react";
import PropTypes from "prop-types";
import { POINTS, PRODUCTS, RESULTS } from "./data";

class ProductQuiz extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedChoices: [],
      numBad: 0,
      score: 0,
      showResults: false,
    };

    this.smallTextClass = "text-font-sans tw-text-xs";
    this.scrollBreakpoint = "large";
  }

  componentDidMount() {
    this.setState({
      numBad: this.state.selectedChoices.filter(
        (choice) => choice.points === POINTS.bad
      ).length,
      score: this.state.selectedChoices.reduce((acc, choice) => {
        return acc + choice.points;
      }, 0),
    });
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevState.selectedChoices !== this.state.selectedChoices) {
      this.setState({
        // find out how many "bad" products are selected
        numBad: this.state.selectedChoices.filter(
          (choice) => choice.points === POINTS.bad
        ).length,
        // calculate the score
        score: this.state.selectedChoices.reduce((acc, choice) => {
          return acc + choice.points;
        }, 0),
      });
    }
  }

  // Handles a product choice being selected or unselected
  // and updates the selectedChoices state accordingly
  handleOptionChange(product, checked) {
    const { selectedChoices } = this.state;

    if (checked) {
      this.setState({ selectedChoices: [...selectedChoices, product] });
    } else {
      this.setState({
        selectedChoices: selectedChoices.filter((o) => o !== product),
      });
    }
  }

  // Handles the form submission
  handleSubmit(event) {
    event.preventDefault();
    this.setState({ showResults: true });
  }

  // Resets the quiz to the initial state
  resetQuiz() {
    this.setState({
      numBad: 0,
      selectedChoices: [],
      showResults: false,
    });
  }

  // Renders a single product choice
  renderChoice(productName, id) {
    const { selectedChoices } = this.state;
    const product = PRODUCTS[productName];

    if (!product) {
      return null;
    }

    return (
      <li key={id} className="tw-relative tw-block">
        <div className="tw-flex tw-items-center tw-mb-0 tw-h-full">
          <input
            type="checkbox"
            name="choice"
            value={productName}
            onChange={(event) =>
              this.handleOptionChange(product, event.target.checked)
            }
            className="tw-hidden tw-peer"
            id={id}
            checked={selectedChoices.includes(product)}
          />
          <label
            htmlFor={id}
            className="
              tw-cursor-pointer tw-flex tw-items-center tw-mb-0 tw-h-full tw-w-full tw-rounded-lg tw-bg-[#F4F4F4] tw-box-border tw-border-2 tw-border-transparent tw-transition-all tw-duration-300 hover:tw-ease-in-out hover:tw-border-blue-20
              peer-checked:tw-border-blue-40 peer-checked:after:tw-text-white peer-checked:after:tw-text-center peer-checked:after:tw-bg-[url('/static/_images/buyers-guide/consumer-creepometer/checkmark.svg')] peer-checked:after:tw-bg-center peer-checked:after:tw-bg-no-repeat peer-checked:after:tw-content-[''] peer-checked:after:tw-absolute peer-checked:after:tw-bg-blue-40 peer-checked:after:tw-rounded-bl-lg peer-checked:after:tw-rounded-tr-lg peer-checked:after:tw-w-[30px] peer-checked:after:tw-h-[25px] peer-checked:after:tw-top-0 peer-checked:after:tw-right-0"
          >
            <div className="tw-w-[48px] tw-h-[48px] tw-m-6">
              <img
                width="100%"
                height="100%"
                src={product.imgSrc}
                alt={product.value}
                className="tw-max-w-full tw-max-h-full tw-object-contain"
              />
            </div>
            <div className="tw-my-6 tw-mr-6">
              <p className={`${this.smallTextClass} tw-text-gray-60 tw-mb-0`}>
                {product.company}
              </p>
              <p className="text-font-sans tw-mb-0 tw-font-light">
                {productName}
              </p>
            </div>
          </label>
        </div>
      </li>
    );
  }

  // Renders the list of product choices
  renderChoices() {
    const { quizChoices } = this.props;

    if (quizChoices === "") {
      return null;
    }

    const choices = quizChoices.split(",").map((productName, index) => {
      productName = productName.trim();

      return this.renderChoice(productName, `product-choice-${index}`);
    });

    if (choices.length === 0) {
      return null;
    }

    return (
      <fieldset className="tw-relative">
        <legend
          className={`tw-sticky ${this.scrollBreakpoint}:tw-static tw-text-center tw-text-base tw-mb-8 medium:tw-mb-[40px]`}
        >
          <div className="tw-font-zilla tw-text-[20px] tw-leading-[24px] medium:tw-text-[28px] mdeium:tw-leading-[36px] tw-font-semibold tw-mb-2">
            Which products do you own?
          </div>
          <small className={`${this.smallTextClass} tw-blcok tw-text-gray-60`}>
            (You can select more than one)
          </small>
        </legend>
        <ul
          className={`tw-h-[60vh] ${this.scrollBreakpoint}:tw-h-auto tw-overflow-y-scroll ${this.scrollBreakpoint}:tw-overflow-y-visible tw-pl-0 tw-pr-10 ${this.scrollBreakpoint}:tw-pr-0 tw-grid tw-grid-cols-1 ${this.scrollBreakpoint}:tw-grid-cols-4 tw-gap-4 ${this.scrollBreakpoint}:tw-gap-8`}
        >
          {choices}
        </ul>
      </fieldset>
    );
  }

  // Renders the quiz form
  renderForm() {
    const { selectedChoices } = this.state;
    return (
      <form onSubmit={(e) => this.handleSubmit(e)}>
        {this.renderChoices()}
        <div
          className={`tw-sticky ${this.scrollBreakpoint}:tw-static tw-mx-auto medium:tw-mt-20 tw-py-8 medium:tw-py-0 tw-text-center`}
        >
          <p className={`${this.smallTextClass} tw-mb-4`}>
            <span>{selectedChoices.length}</span>{" "}
            {selectedChoices.length > 1 ? "Products" : "Product"} Selected
          </p>
          <button
            className="tw-btn tw-btn-primary tw-mb-8 tw-w-full large:tw-w-auto"
            type="submit"
            onSubmit={(e) => this.handleSubmit(e)}
          >
            See Results
          </button>
          <p className={`${this.smallTextClass} tw-text-gray-60 tw-mb-0`}>
            Your score will not be recorded in our system and no personal data
            will be collected.
          </p>
        </div>
      </form>
    );
  }

  // Renders the results screen
  renderResults() {
    const { selectedChoices, score } = this.state;

    let resultType = null;

    if (
      score >= RESULTS["open book"].minPoints ||
      (selectedChoices.length > 0 &&
        selectedChoices.length === this.state.numBad)
    ) {
      resultType = RESULTS["open book"];
    } else if (score >= RESULTS["soso"].minPoints) {
      resultType = RESULTS["soso"];
    } else {
      resultType = RESULTS["off the grid"];
    }

    return (
      <div className="tw-flex tw-flex-col medium:tw-flex-col-reverse tw-dark">
        <div className="tw-text-center">
          <div className="tw-mx-auto tw-w-[80px] tw-h-[80px] medium:tw-w-[180px] medium:tw-h-[180px]">
            <img src={resultType.imgSrc} alt="" width="100%" height="100%" />
          </div>
          <h3 className="tw-font-zilla tw-font-semibold tw-text-[28px] tw-leading-[36px] medium:tw-text-[48px] medium:tw-leading-[56px] tw-text-white tw-my-12 medium:tw-mt-16">
            {resultType.heading}
          </h3>
          <p className="tw-text-white">{resultType.description}</p>
          <div className="tw-mt-[84px] medium:mt-[100px] tw-text-red-60">
            [FIXME] will add social share buttons in follow-up PR
          </div>
        </div>
        <div className="tw-text-center medium:tw-text-right tw-mt-12 medium:tw-mt-0">
          <button
            className="tw-btn tw-btn-secondary tw-w-full medium:tw-w-auto"
            onClick={(e) => this.resetQuiz(e)}
          >
            Retake Quiz
          </button>
        </div>
      </div>
    );
  }

  render() {
    const { showResults, selectedChoices, score } = this.state;
    const outerClass = showResults
      ? "tw-bg-blue-40 tw-px-14 tw-py-16 medium:tw-p-24"
      : "tw-bg-white tw-my-24 tw-px-[15px] tw-py-16 medium:tw-px-[45px] medium:tw-py-24";

    return (
      <div className={`${outerClass} tw-rounded-3xl tw-my-24`}>
        {showResults ? this.renderResults() : this.renderForm()}

        <div className="tw-border-4 tw-border-red-60 tw-mt-24 tw-p-10">
          <p className="tw-text-red-60 tw-font-bold">
            This box is for QA purposes. Will remove before merging the PR.
          </p>
          <p className="tw-font-bold tw-mb-0">Score: {score}</p>
          <p className="tw-font-bold">
            {this.state.numBad} of {selectedChoices.length} products selected
            were bad products.
          </p>
          <p>Selected:</p>
          <ul>
            {selectedChoices.map((product, i) => (
              <li key={i}>
                {product.name} {product.points === POINTS.bad && "(bad)"}
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
}

ProductQuiz.propTypes = {
  quizChoices: PropTypes.string, // comma separated list of product names
};

ProductQuiz.defaultProps = {
  quizChoices: "",
};

export default ProductQuiz;
