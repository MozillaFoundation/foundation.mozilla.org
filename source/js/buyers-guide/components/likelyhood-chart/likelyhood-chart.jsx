// TODO: Inject likely % in .bar and .likelyhood-words

import React from 'react';

export default class LikelyhoodChart extends React.Component {
  constructor(props) {
    super(props);
  }

  render(){
    let values = this.props.values;
    let total = values[0] + values[1];
    let perc = Math.round(100 * values[0]/total, 10);

    return (
      <div>
        <table id="likelyhood-score">
          <tbody>
            <tr className="likely">
              <th>
                <span className="likely-label">Likely</span>
              </th>
              <td className="likelyhood">
                <span className="bar" style={{width: `${100 - perc}%`,}}></span>
                <span className="likelyhood-words">{100 - perc}% Likely to buy it</span>
              </td>
            </tr>
            <tr className="unlikely">
              <th>
                <span className="likely-label">Not likely</span>
              </th>
              <td className="likelyhood">
                <span className="bar" style={{width: `${perc}%`,}}></span>
                <span className="likelyhood-words">{perc}% Not likely to buy it</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  }
}
