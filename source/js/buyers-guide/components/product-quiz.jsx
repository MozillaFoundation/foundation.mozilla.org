import React, { Component } from "react";
import PropTypes from "prop-types";

const IMG_DIR = "/static/_images/buyers-guide/consumer-creepometer";

const POINTS = {
  good: 0,
  soso: 1,
  bad: 2,
};

const PRODUCTS = {
  Signal: {
    name: "Signal",
    company: "Signal Foundation",
    imgSrc: `${IMG_DIR}/products/Signal.png`,
    points: POINTS.good,
  },
  "SL Speakers": {
    name: "SL Speakers",
    company: "Sonos",
    imgSrc: `${IMG_DIR}/products/Sonos_SL_Speakers.png`,
    points: POINTS.good,
  },
  "Garmin Fenix": {
    name: "Garmin Fenix",
    company: "Garmin",
    imgSrc: `${IMG_DIR}/products/Garmin_Fenix.png`,
    points: POINTS.good,
  },
  "Nintendo Switch": {
    name: "Nintendo Switch",
    company: "Nintendo",
    imgSrc: `${IMG_DIR}/products/Nintendo_Switch.png`,
    points: POINTS.good,
  },
  "Nvidia Shield TV": {
    name: "Nvidia Shield TV",
    company: "Nvidia",
    imgSrc: `${IMG_DIR}/products/Nvidia_Shield_TV.png`,
    points: POINTS.good,
  },
  "Apple Watch": {
    name: "Apple Watch",
    company: "Apple",
    imgSrc: `${IMG_DIR}/products/Apple_Watch.png`,
    points: POINTS.soso,
  },
  Telegram: {
    name: "Telegram",
    company: "Telegram FZ-LLC",
    imgSrc: `${IMG_DIR}/products/Telegram.png`,
    points: POINTS.soso,
  },
  "Tile Trackers": {
    name: "Tile Trackers",
    company: "Tile",
    imgSrc: `${IMG_DIR}/products/Tile_Trackers.png`,
    points: POINTS.soso,
  },
  "Google Hangouts": {
    name: "Google Hangouts",
    company: "Google",
    imgSrc: `${IMG_DIR}/products/Google_Hangouts.png`,
    points: POINTS.soso,
  },
  "Video Doorbells": {
    name: "Video Doorbells",
    company: "Google Nest",
    imgSrc: `${IMG_DIR}/products/Google_Nest_Video_Doorbell.png`,
    points: POINTS.soso,
  },
  "Facebook Portal": {
    name: "Facebook Portal",
    company: "Facebook",
    imgSrc: `${IMG_DIR}/products/Facebook_Portal.png`,
    points: POINTS.bad,
  },
  "Echo Studio": {
    name: "Echo Studio",
    company: "Amazon",
    imgSrc: `${IMG_DIR}/products/Amazon_Echo_Studio.png`,
    points: POINTS.bad,
  },
  "Ring Security Cam": {
    name: "Ring Security Cam",
    company: "Amazon",
    imgSrc: `${IMG_DIR}/products/Amazon_Ring_Security_Camera.png`,
    points: POINTS.bad,
  },
  WeChat: {
    name: "WeChat",
    company: "Tencent",
    imgSrc: `${IMG_DIR}/products/WeChat.png`,
    points: POINTS.bad,
  },
  "Streaming Sticks": {
    name: "Streaming Sticks",
    company: "Roku",
    imgSrc: `${IMG_DIR}/products/Roku_Streaming_Sticks.png`,
    points: POINTS.bad,
  },
  Nook: {
    name: "Nook",
    company: "Barnes and Noble",
    imgSrc: `${IMG_DIR}/products/Barnes_Noble_Nook.png`,
    points: POINTS.bad,
  },
};

const RESULTS = {
  "open book": {
    minPoints: 9,
    heading: "You’re an open book.",
    description:
      "You’re an open book. The products and apps you use collect a lot of your personal information. Data brokers send their thanks! But don’t worry — you’re not alone. Even the privacy researchers at Mozilla use some of the same products and apps. If you’re uncomfortable with your quiz results, try opting out of data sharing whenever possible. And choose alternative tech that is more privacy conscious: privacynotincluded.org",
    imgSrc: `${IMG_DIR}/emoji-open-book.png`,
  },
  soso: {
    minPoints: 5,
    heading: "Your privacy is so-so.",
    description:
      "Your privacy is so-so. Your online privacy could be worse — but it could be better, too. While some of the products and apps you use value privacy, others are collecting and sharing a good amount of personal data. If you’re okay with that balance, no problem. If you’d like a little more privacy, find alternatives: privacynotincluded.org",
    imgSrc: `${IMG_DIR}/emoji-soso.png`,
  },
  "off the grid": {
    minPoints: 0,
    heading: "You’re off the grid.",
    description:
      "You’re off the grid. Woah — you take your online privacy and security seriously. That’s no easy feat these days, when everything from connected litterboxes to smart water bottles are after your data. When you get a break from scouring privacy policies and encrypting all the things, why not share some privacy tips with your friends and family? privacynotincluded.org",
    imgSrc: `${IMG_DIR}/emoji-off-the-grid.png`,
  },
};

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
              tw-cursor-pointer tw-flex tw-items-center tw-mb-0 tw-h-full tw-w-full tw-rounded-lg tw-bg-[#F4F4F4] tw-box-border tw-border-2 tw-border-transparent hover:tw-border-blue-20
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
      <fieldset className="tw-h-[60vh] medium:tw-h-auto tw-overflow-y-scroll medium:tw-overflow-y-visible">
        <legend className="tw-sticky medium:tw-static tw-text-center tw-text-base tw-mb-8 medium:tw-mb-[40px]">
          <div className="tw-font-zilla tw-text-[20px] tw-leading-[24px] medium:tw-text-[28px] mdeium:tw-leading-[36px] tw-font-semibold tw-mb-2">
            Which products do you own?
          </div>
          <small className={`${this.smallTextClass} tw-blcok tw-text-gray-60`}>
            (You can select more than one)
          </small>
        </legend>
        <ul className="tw-pl-0 tw-grid tw-grid-cols-1 large:tw-grid-cols-4 tw-gap-6 large:tw-gap-8">
          {choices}
        </ul>
      </fieldset>
    );
  }

  renderForm() {
    const { selectedChoices } = this.state;
    return (
      <form onSubmit={(e) => this.handleSubmit(e)}>
        {this.renderChoices()}
        <div className="tw-sticky medium:tw-static tw-mx-auto medium:tw-mt-20 tw-py-8 medium:tw-py-0 tw-text-center">
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
