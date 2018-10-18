import React from 'react';

export default class CreepChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    let values = this.props.values;
    let data = [
      {c: 'no-creep', label: 'Not creepy', value: values[0], offset: 0},
      {c: 'little-creep', label: 'A little creepy', value: values[1], offset: 225},
      {c: 'somewhat-creep', label: 'Somewhat creepy', value: values[2], offset: 475},
      {c: 'very-creep', label: 'Very creepy', value: values[3], offset: 725},
      {c: 'super-creep', label: 'Super creepy', value: values[4], offset: 975}
    ];
    let sum = data.reduce((tally, v) => tally + v.value, 0);

    return {
      totalCreepiness: sum,
      creepinessData: data
    };
  }

  render() {
    return (
      <div>
        <table id="creepiness-score">
          <tbody>
            {
              this.state.creepinessData.map(data => {
                let percent = Math.round(100 * data.value / this.state.totalCreepiness);
                console.log(data.value, this.state.totalCreepiness, percent);
                return (
                  <tr key={data.c} className={`your-vote ${data.c}`}>
                    <th>
                      <div className="bar" style={{height: `${percent}px`}}></div>
                      <span className="creep-label">{data.label}</span>
                      <span className="creep-face" style={{backgroundPositionY: `-${data.offset}px`}}></span>
                    </th>
                    <td className="creepiness">{percent}%</td>
                  </tr>
                );
              })
            }
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
