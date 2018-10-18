import React from 'react';
import Creepometer from '../creepometer/creepometer.jsx';
import CreepChart from '../creepiness-chart/creepiness-chart.jsx';
import LikelyhoodChart from '../likelyhood-chart/likelyhood-chart.jsx';

export default class CreepVote extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
    console.log(this.props.votes);
  }

  getInitialState() {
    let conf = this.props.votes.confidence;
    let totalVotes = conf[0] + conf[1];

    return {
      totalVotes,
      creepiness: 50,
      confidence: undefined,
      didVote: false
    };
  }

  showVoteResult() {
    if (this.state.creepinessSubmitted && this.state.confidenceSubmitted) {
      this.setState({ didVote: true });
    }
  }

  sendVoteFor(payload) {
    let attribute = payload.attribute;
    let url = "/privacynotincluded/vote";
    let method = "POST";
    let credentials = 'same-origin';
    let headers = {
      "X-CSRFToken": this.props.csrf,
      "Content-Type": "application/json"
    };

    fetch(url, {
      method,
      credentials,
      headers,
      body: JSON.stringify(payload)
    })
    .then(response => {
      let update = {};
      update[`${attribute}Submitted`] = true;
      this.setState(update, () => {
        this.showVoteResult()
      });
    })
    .catch(e => {
      console.warn(e);
      this.setState({ disableVoteButton: false });
    });
  }

  submitVote(evt) {
    evt.preventDefault();

    let confidence = this.state.confidence;

    if (confidence === undefined) {
      return;
    }

    this.setState({ disableVoteButton: true });

    let productID = this.props.productID;

    this.sendVoteFor({
      attribute: 'confidence',
      productID,
      value: confidence,
    });

    this.sendVoteFor({
      attribute: 'creepiness',
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
    return (<form method="post" id="creep-vote" onSubmit={evt => this.submitVote(evt)}>
      <div className="row mb-5">
        <div className="col-12 col-md-6">
          <div className="mb-4 text-center">
            <h3 className="h5-heading mb-2">How creepy is this product?</h3>
            <p>Majority of voters think it is super creepy</p>
          </div>
          <Creepometer initialValue={this.state.creepiness} onChange={value => this.setCreepiness(value)}></Creepometer>
        </div>
        <div className="col-12 col-md-6">
          <div className="mb-4 text-center">
            <h3 className="h5-heading mb-2">How likely are you to buy it?</h3>
            <p>Majority of voters are not likely to buy it</p>
          </div>
          <div className="text-center">
            <div class="btn-group btn-group-toggle" data-toggle="buttons">
              <label for="likely">
                <input type="radio" name="wouldbuy" id="likely" autocomplete="off" required/>
                <span class="btn" onClick={evt => this.setConfidence(true)}>Likely</span>
              </label>
              <label for="unlikely">
                <input type="radio" name="wouldbuy" id="unlikely" autocomplete="off" required/>
                <span class="btn" onClick={evt => this.setConfidence(false)}>Not likely</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-12 text-center">
          <button type="submit" className="btn btn-ghost mb-2" disabled={this.state.confidence===undefined}>Vote & See Results</button>
          <p>{this.state.totalVotes} votes</p>
        </div>
      </div>
    </form>);
  }

  /**
   * @returns {jsx} What users see when they have voted on this product.
   */
  renderDidVote(){
    return(
      <div>
        <div className="mb-5">
          <div className="col-12 text-center">
            <h3 className="h4-heading">Thanks for voting! Here are the results so far:</h3>
            <div>{this.state.totalVotes} Votes</div>
          </div>
          <div className="row">
            <div className="col">
              <CreepChart values={this.props.votes.creepiness.vote_breakdown} />
            </div>
            <div className="col likelyhood-chart">
              <LikelyhoodChart values={this.props.votes.confidence} />
            </div>
          </div>
        </div>
      </div>
    );
  }

  render() {
    let voteContent;

    if(this.state.didVote){
      voteContent = this.renderDidVote();
    } else {
      voteContent = this.renderVoteAsk();
    }

    return (
      <div className="creep-vote py-5">
        { voteContent }
        <div>View comments or share your results</div>
        {/* TODO: Make these share links work */}
        <div className="share-links">fb, tw, email</div>
      </div>
    );
  }
}
