import React from 'react';
import Creepometer from '../creepometer/creepometer.jsx';

export default class CreepVote extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    return (
      <div className="creep-vote py-5">
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
              <button>Likely</button>
              <button>Not likely</button>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-12 text-center">
            <button className="btn btn-ghost mb-2">Vote & See Results</button>
            <p>367 votes</p>
          </div>
        </div>
      </div>
    );
  }
}
