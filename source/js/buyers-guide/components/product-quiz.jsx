import React, { useState, useEffect } from "react";
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

function ProductQuiz(props) {
  console.log("propsss", props);

  const [selectedOptions, setSelectedOptions] = useState([]);
  const [numBad, setNumBad] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(true);
  const smallTextClass = "text-font-sans tw-text-xs";

  function handleOptionChange(product, checked) {
    if (checked) {
      setSelectedOptions([...selectedOptions, product]);
    } else {
      setSelectedOptions(selectedOptions.filter((o) => o !== product));
    }
  }

  console.log(`selectedOptions`, selectedOptions);
  selectedOptions.forEach((product) => console.log(`selected:`, product));

  useEffect(() => {
    setNumBad(
      selectedOptions.filter((option) => option.points === POINTS.bad).length
    );
    let finalScore = selectedOptions.reduce((acc, option) => {
      return acc + option.points;
    }, 0);

    console.log(`>>>>`, finalScore);
    setScore(finalScore);
  }, [selectedOptions]);

  function handleSubmit(event) {
    event.preventDefault();
    setShowResults(true);
  }

  function resetQuiz() {
    setNumBad(0);
    setSelectedOptions([]);
    setShowResults(false);
  }

  function renderChoices() {
    let choices = props.quizChoices.split(",").map((choice) => choice.trim());
    console.log(choices);

    let listItems = choices.map((name, index) => {
      const id = `product-choice-${index}`;
      const product = PRODUCTS[name];

      if (!product) {
        return null;
      }

      return (
        <li key={id} className="tw-relative tw-block">
          <div className="tw-flex tw-items-center tw-mb-0 tw-h-full">
            <input
              type="checkbox"
              name="choice"
              value={name}
              onChange={(event) =>
                handleOptionChange(product, event.target.checked)
              }
              className="tw-hidden tw-peer"
              id={id}
              checked={selectedOptions.includes(product)}
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
                <p className={`${smallTextClass} tw-text-gray-60 tw-mb-0`}>
                  {product.company}
                </p>
                <p className="text-font-sans tw-mb-0 tw-font-light">{name}</p>
              </div>
            </label>
          </div>
        </li>
      );
    });

    if (listItems.length === 0) {
      return null;
    }

    return (
      <ul className="tw-grid tw-grid-cols-4 tw-gap-6 medium:tw-gap-8 tw-pl-0">
        {listItems}
      </ul>
    );
  }

  function renderResults() {
    let resultType = null;

    if (
      score >= RESULTS["open book"].minPoints ||
      (selectedOptions.length > 0 && selectedOptions.length === numBad)
    ) {
      resultType = RESULTS["open book"];
    } else if (score >= RESULTS["soso"].minPoints) {
      resultType = RESULTS["soso"];
    } else {
      resultType = RESULTS["off the grid"];
    }

    // console.log(score, `resultType = `, resultType);
    return (
      <div className="tw-text-center tw-bg-blue-40 tw-p-24">
        <h1 className="tw-text-white">Your Score: {score}</h1>
        <img src={resultType.imgSrc} alt="" className="tw-mx-auto" />
        <h3 className="tw-font-zilla tw-font-semibold tw-text-[48px] tw-leading-[56px] tw-text-white tw-mt-16 tw-mb-12">
          {resultType.heading}
        </h3>
        <p className="tw-text-white">{resultType.description}</p>
      </div>
    );
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {renderChoices()}
        <div className="tw-mx-auto tw-mt-20 tw-text-center">
          <p className={`${smallTextClass} tw-mb-4`}>
            <span>{selectedOptions.length}</span>{" "}
            {selectedOptions.length > 1 ? "Products" : "Product"} Selected
          </p>
          <button
            className="tw-btn tw-btn-primary tw-mb-8"
            type="submit"
            onSubmit={handleSubmit}
          >
            See Results
          </button>
          <p className={`${smallTextClass} tw-text-gray-60 tw-mb-0`}>
            Your score will not be recorded in our system and no personal data
            will be collected.
          </p>
        </div>
      </form>
      {showResults && renderResults()}
      {showResults && (
        <div>
          <p>
            {numBad} of {selectedOptions.length} products selected were bad
            products.
          </p>
          <p>Selected:</p>
          <ul>
            {selectedOptions.map((product, i) => (
              <li key={i}>
                {product.name} {product.points === POINTS.bad && "(bad)"}
              </li>
            ))}
          </ul>
          <button className="tw-btn tw-btn-primary" onClick={resetQuiz}>
            Retake Quiz
          </button>
        </div>
      )}
    </div>
  );
}

ProductQuiz.propTypes = {
  quizChoices: PropTypes.string, // comma separated list of product names
};

ProductQuiz.defaultProps = {
  quizChoices: "",
};

export default ProductQuiz;
