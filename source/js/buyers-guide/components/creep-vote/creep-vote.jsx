import { Component, Fragment } from "react";
import Creepometer from "../creepometer/creepometer.jsx";
import CreepChart from "../creepiness-chart/creepiness-chart.jsx";
import SocialShare from "../social-share/social-share.jsx";
import JoinUs from "../../../components/join/join.jsx";
import { getText } from "../../../components/petition/locales";

import CREEPINESS_LABELS from "../creepiness-labels.js";

/**
 * PNI creep vote component.
 * Submits user's creepiness vote for a product and shows aggregated result after.
 */
class CreepVote extends Component {
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

    Object.keys(creepBreakdown).forEach((id) => {
      let v = creepBreakdown[id];

      if (v > creepiness) {
        creepiness = v;
        creepinessId = id;
      }
    });

    let subscribed = sessionStorage.subscribed === "true";
    let voteCount = parseInt(sessionStorage.getItem(`voteCount`) || 0);

    if (voteCount >= 3) {
      subscribed = true;
    }

    sessionStorage.setItem("subscribed", subscribed);

    return {
      totalVotes,
      creepiness: 50,
      hasMoved: false,
      didVote: false,
      majority: {
        creepiness: creepinessId,
      },
      subscribed,
      showNewsletter: false,
      voteCount,
    };
  }

  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  showVoteResult() {
    const { creepinessSubmitted, voteCount } = this.state;

    if (creepinessSubmitted) {
      this.setState({
        showNewsletter: voteCount === 2 || voteCount === 3,
        didVote: true,
      });
    }
  }

  sendVoteFor(payload) {
    let attribute = payload.attribute;
    // by default, we'll be posting to the PNI Django app posting route (see its views.py)
    let url = `/api/buyersguide/vote/`;

    // If we're running for the new wagtail version of PNI, voting is a post to the product's URL instead.
    if (document.getElementById("product-research").dataset.isWagtailPage) {
      url = ".";
    }
    let method = `POST`;
    let credentials = `same-origin`;
    let headers = {
      "X-CSRFToken": this.props.csrf,
      "Content-Type": `application/json`,
    };

    fetch(url, {
      method,
      credentials,
      headers,
      body: JSON.stringify(payload),
    })
      .then(() => {
        let update = {};

        update[`${attribute}Submitted`] = true;
        this.setState(update, () => {
          this.showVoteResult();
        });
      })
      .catch((e) => {
        console.warn(e);
      });
  }

  submitVote(evt) {
    evt.preventDefault();

    let voteCount = this.state.voteCount + 1;
    sessionStorage.setItem("voteCount", voteCount);
    this.setState({ voteCount });

    let productID = this.props.productID;

    this.sendVoteFor({
      attribute: `creepiness`,
      productID,
      value: this.state.creepiness,
    });
  }

  setCreepiness(creepiness) {
    this.setState({ creepiness });
  }

  handleSignUp(successState) {
    sessionStorage.setItem("subscribed", successState);
    this.setState({ showNewsletter: false, subscribed: successState });
  }

  /**
   * @returns {jsx} What users see when they haven't voted on this product yet.
   */
  renderVoteAsk() {
    return (
      <Fragment>
        <form
          method="post"
          id="creep-vote"
          onSubmit={(evt) => this.submitVote(evt)}
        >
          <div className="row mb-5">
            <div className="col-12">
              <div className="mb-4 text-center">
                <h3 className="h3-heading mb-2">
                  How creepy do you think this is?
                </h3>
              </div>
              <Creepometer
                initialValue={this.state.creepiness}
                toggleMoved={() => this.setState({ hasMoved: true })}
                onChange={(value) => this.setCreepiness(value)}
              />
            </div>
          </div>
          <div className="row">
            <div className="col-12 text-center">
              <button
                id="creep-vote-btn"
                type="submit"
                className="btn btn-pop mb-2"
                disabled={!this.state.hasMoved}
              >
                Vote & see results
              </button>
              <p className="h6-heading mb-0">{this.state.totalVotes} votes</p>
            </div>
          </div>
        </form>
      </Fragment>
    );
  }

  /**
   * @returns {jsx} Sign up ask in the middle of vote if user is not already subscribed
   * or if they haven't voted multiple times.
   */

  renderSignUp() {
    return (
      <Fragment>
        <button
          className="btn btn-close-sign-up text-uppercase d-flex justify-content-between align-items-center"
          onClick={() => this.handleSignUp(false)}
          type="button"
        >
          Close
        </button>
        <JoinUs
          formPosition="flow"
          flowHeading={getText(`You voted! You rock!`)}
          flowText={getText(
            `Now that you’re on a roll, why not join Mozilla? We’re not creepy (we promise). We actually fight back against creepy. And we need more people like you.`
          )}
          csrfToken={this.props.joinUsCSRF}
          apiUrl={this.props.joinUsApiUrl}
          handleSignUp={(successState) => this.handleSignUp(successState)}
        />
      </Fragment>
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
            <h3 className="h3-heading mb-1">
              {this.state.totalVotes + 1} Votes — invite your friends!
            </h3>
            <div className="h6-heading text-muted" />
          </div>
          <div className="row mt-4">
            <div className="col-12">
              <CreepChart
                userVoteGroup={userVoteGroup}
                values={this.props.votes.creepiness.vote_breakdown}
              />
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
    const { didVote, showNewsletter } = this.state;
    let content = this.renderVoteAsk();

    if (didVote) {
      content = this.renderDidVote();

      if (showNewsletter) {
        content = this.renderSignUp();
      }
    }

    return <div className="creep-vote">{content}</div>;
  }
}

export default CreepVote;
