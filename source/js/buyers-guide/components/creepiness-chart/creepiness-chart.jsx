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
      <table id="creepiness-score">
        <tbody>
          <tr><th><div className="bar" style={{height: '50px'}}></div><span className="creep-face">a</span></th><td className="creepiness">1%</td></tr>
          <tr><th><div className="bar" style={{height: '0px'}}></div><span className="creep-face">b</span></th><td className="creepiness">2%</td></tr>
          <tr><th><div className="bar" style={{height: '40px'}}></div><span className="creep-face">c</span></th><td className="creepiness">3%</td></tr>
          <tr><th><div className="bar" style={{height: '25px'}}></div><span className="creep-face">d</span></th><td className="creepiness">4%</td></tr>
          <tr><th><div className="bar" style={{height: '65px'}}></div><span className="creep-face">e</span></th><td className="creepiness">5%</td></tr>
        </tbody>
      </table>
    );
  }
}
