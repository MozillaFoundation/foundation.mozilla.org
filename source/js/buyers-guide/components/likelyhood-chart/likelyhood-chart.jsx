// TODO: Inject likely % in .bar and .likelyhood-words

import React from 'react';

export default class LikelyhoodChart extends React.Component {
  constructor(props) {
    super(props);

    this.state = this.getInitialState();

  }

  getInitialState() {
    return {
    };
  }

  render(){
    return (
      <div>
        <table id="likelyhood-score">
          <tbody>
            <tr className="likely">
              <th>
                <span className="likely-label">Likely</span>
              </th>
              <td className="likelyhood">
                <span className="bar" style={{width: '95%'}}></span>
                <span className="likelyhood-words">95% Likely to buy it</span>
              </td>
            </tr>
            <tr className="unlikely">
              <th>
                <span className="likely-label">Not likely</span>
              </th>
              <td className="likelyhood">
                <span className="bar" style={{width: '5%'}}></span>
                <span className="likelyhood-words">5% Not likely to buy it</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  }
}
