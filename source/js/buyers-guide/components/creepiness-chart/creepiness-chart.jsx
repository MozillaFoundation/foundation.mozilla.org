import React from 'react';

export default class CreepChart extends React.Component {
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
        <table id="creepiness-score">
          <tbody>
            {/* TODO: Pull in vote% and apply as pixel height, td value.
            TODO: Apply "your-vote" class to the level of the user's vote  */}
            <tr className="your-vote no-creep">
              <th>
                <div className="bar" style={{height: '100px'}}></div>
                <span className="creep-label">Not creepy</span>
                <span className="creep-face"></span>
              </th>
              <td className="creepiness">1%</td>
            </tr>
            <tr className="your-vote little-creep">
              <th>
                <div className="bar" style={{height: '20px'}}></div>
                <span className="creep-label">A little creepy</span>
                <span className="creep-face"></span>
              </th>
              <td className="creepiness">2%</td>
            </tr>
            <tr className="your-vote somewhat-creep">
              <th>
                <div className="bar" style={{height: '40px'}}></div>
                <span className="creep-label">Somewhat creepy</span>
                <span className="creep-face"></span>
              </th>
              <td className="creepiness">3%</td>
            </tr>
            <tr className="your-vote very-creep">
              <th>
                <div className="bar" style={{height: '25px'}}></div>
                <span className="creep-label">Very creepy</span>
                <span className="creep-face"></span>
              </th>
              <td className="creepiness">4%</td>
            </tr>
            <tr className="your-vote super-creep">
              <th>
                <div className="bar" style={{height: '65px'}}></div>
                <span className="creep-label">Super creepy</span>
                <span className="creep-face"></span>
              </th>
              <td className="creepiness">5%</td>
            </tr>
          </tbody>
        </table>
        <div className="row">
          <div className="col text-left text-muted">Not creepy</div>
          <div className="col text-right text-muted">Super creepy</div>
        </div>
      </div>
    );
  }
}
