import React from 'react';
import Creepometer from '../creepometer/creepometer.jsx';
import CreepChart from '../creepiness-chart/creepiness-chart.jsx';

export default class CreepVote extends React.Component {
  constructor(props) {
    super(props);

    this.state = this.getInitialState();

    this.submitVote = this.submitVote.bind(this);
  }

  getInitialState() {
    return {
      didVote: false
    };
  }

  submitVote(){
    this.setState({didVote:true});
  }

  /**
   * @returns {jsx} What users see when they haven't voted on this product yet.
   */
  renderVoteAsk() {
    return (<form method="post" id="creep-vote" onSubmit={this.submitVote}>
      <div className="row mb-5">
        <div className="col-12 col-md-6">
          <div className="mb-4 text-center">
            <h3 className="h5-heading mb-2">How creepy is this product?</h3>
            <p>Majority of voters think it is super creepy</p>
          </div>
          <Creepometer initialValue={50}></Creepometer>
        </div>
        <div className="col-12 col-md-6">
          <div className="mb-4 text-center">
            <h3 className="h5-heading mb-2">How likely are you to buy it?</h3>
            <p>Majority of voters are not likely to buy it</p>
          </div>
          <div className="text-center">
            <div class="btn-group btn-group-toggle" data-toggle="buttons">
              <label for="likely">
                <input type="radio" name="wouldbuy" id="likely" autocomplete="off" required /><span class="btn">Likely</span>
              </label>
              <label for="unlikely">
                <input type="radio" name="wouldbuy" id="unlikely" autocomplete="off" required /><span class="btn">Not likely</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-12 text-center">
          <button type="submit" className="btn btn-ghost mb-2">Vote & See Results</button>
          <p>367 votes</p>
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
            <h3 className="h4-heading">Thanks for voting! Here are the results</h3>
            <div>367 Votes</div>
          </div>
          <div className="row">
            <div className="col"><CreepChart/></div>
            <div className="col likelyhood-chart">10% likely to buy</div>
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
      </div>
    );
  }
}
