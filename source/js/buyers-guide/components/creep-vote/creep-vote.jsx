import React from "react";
import classNames from "classnames";
import Creepometer from "../creepometer/creepometer.jsx";
import CreepChart from "../creepiness-chart/creepiness-chart.jsx";
import LikelyhoodChart from "../likelyhood-chart/likelyhood-chart.jsx";
import SocialShare from "../social-share/social-share.jsx";

import CREEPINESS_LABELS from "../creepiness-labels.js";

export default class CreepVote extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    let votes = this.props.votes;
    let totalVotes = votes.total;

    let creepBreakdown = votes.creepiness.vote_breakdown;
    let creepiness = 0;
    let creepinessId = 0;

    Object.keys(creepBreakdown).forEach(id => {
      let v = creepBreakdown[id];

      if (v > creepiness) {
        creepiness = v;
        creepinessId = id;
      }
    });

    let confidence = votes.confidence;

    return {
      totalVotes,
      creepiness: 50,
      confidence: undefined,
      didVote: false,
      majority: {
        creepiness: creepinessId,
        confidence: confidence[0] > confidence[1] ? 0 : 1
      }
    };
  }

  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  showVoteResult() {
    if (this.state.creepinessSubmitted && this.state.confidenceSubmitted) {
      this.setState({ didVote: true });
    }
  }

  sendVoteFor(payload) {
    let attribute = payload.attribute;
    let url = `/api/buyersguide/vote/`;
    let method = `POST`;
    let credentials = `same-origin`;
    let headers = {
      "X-CSRFToken": this.props.csrf,
      "Content-Type": `application/json`
    };

    fetch(url, {
      method,
      credentials,
      headers,
      body: JSON.stringify(payload)
    })
      .then(() => {
        let update = {};

        update[`${attribute}Submitted`] = true;
        this.setState(update, () => {
          this.showVoteResult();
        });
      })
      .catch(e => {
        console.warn(e);
      });
  }

  submitVote(evt) {
    evt.preventDefault();

    let confidence = this.state.confidence;
    let productID = this.props.productID;

    this.sendVoteFor({
      attribute: `confidence`,
      productID,
      value: confidence
    });

    this.sendVoteFor({
      attribute: `creepiness`,
      productID,
      value: this.state.creepiness
    });
  }

  setCreepiness(creepiness) {
    this.setState({ creepiness });
  }

  setConfidence(confidence) {
    this.setState({ confidence });
  }

  /**
   * @returns {jsx} What users see when they haven't voted on this product yet.
   */
  renderVoteAsk() {
    let unlikelyClasses = classNames("unlikely-glyph btn btn-secondary", {
      selected: this.state.confidence == false
    });

    let likelyClasses = classNames("likely-glyph btn btn-secondary", {
      selected: this.state.confidence == true
    });

    return (
      <form
        method="post"
        id="creep-vote"
        onSubmit={evt => this.submitVote(evt)}
      >
        <div className="row mb-5">
          <div className="col-12 col-md-6">
            <div className="mb-4 text-center">
              <h3 className="h5-heading mb-2">
                How creepy do you think this is?
              </h3>
            </div>
            <Creepometer
              initialValue={this.state.creepiness}
              onChange={value => this.setCreepiness(value)}
            />
          </div>
          <div className="col-12 col-md-6 mt-5 mt-md-0">
            <div className="mb-4 text-center">
              <h3 className="h5-heading mb-2">How likely are you to buy it?</h3>
            </div>
            <div className="text-center">
              <div
                class="btn-group btn-group-toggle mt-3 mt-md-5"
                data-toggle="buttons"
              >
                <label for="likely">
                  <input
                    type="radio"
                    name="wouldbuy"
                    id="likely"
                    autocomplete="off"
                  />
                  <span
                    className={likelyClasses}
                    onClick={() => this.setConfidence(true)}
                  >
                    Likely
                  </span>
                </label>
                <label for="unlikely">
                  <input
                    type="radio"
                    name="wouldbuy"
                    id="unlikely"
                    autocomplete="off"
                  />
                  <span
                    className={unlikelyClasses}
                    onClick={() => this.setConfidence(false)}
                  >
                    Not likely
                  </span>
                </label>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-12 text-center">
            <button
              id="creep-vote-btn"
              type="submit"
              className="btn btn-secondary mb-2"
            >
              Vote & See Results
            </button>
            <p class="h6-heading mb-0">{this.state.totalVotes} votes</p>
          </div>
        </div>
      </form>
    );
  }

  /**
   * @returns {jsx} What users see when they have voted on this product.
   */
  renderDidVote() {
    let bins = CREEPINESS_LABELS.length;
    let userVoteGroup = Math.floor((bins * (this.state.creepiness - 1)) / 100);
    let creepType = CREEPINESS_LABELS[userVoteGroup];

    return (
      <div>
        <div className="mb-5">
          <div className="col-12 text-center">
            <h3 className="h2-heading mb-1">
              {this.state.totalVotes + 1} Votes — invite your friends!
            </h3>
            <div className="h6-heading text-muted" />
          </div>
          <div className="row mt-4">
            <div className="col-12 col-lg-11 d-md-flex m-md-auto align-items-md-center">
              <div className="px-0 px-lg-3 col-lg-7 mb-5 mb-md-0 creep-chart">
                <CreepChart
                  userVoteGroup={userVoteGroup}
                  values={this.props.votes.creepiness.vote_breakdown}
                />
              </div>
              <div className="col likelyhood-chart d-flex justify-content-center">
                <LikelyhoodChart values={this.props.votes.confidence} />
              </div>
            </div>
          </div>
        </div>
        <SocialShare
          productName={this.props.productName}
          creepType={creepType}
        />
      </div>
    );
  }

  render() {
    let voteContent;

    if (this.state.didVote) {
      voteContent = this.renderDidVote();
    } else {
      voteContent = this.renderVoteAsk();
    }

    return (
      <div className="creep-vote my-5">
        <div class="what-you-think-label h5-heading d-inline-block">
          Tell us what you think
        </div>
        {voteContent}
      </div>
    );
  }
}
