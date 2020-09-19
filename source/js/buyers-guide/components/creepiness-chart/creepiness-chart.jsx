import React from "react";
import CREEPINESS_LABELS from "../creepiness-labels.js";

export default class CreepChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    let values = this.props.values;
    let data = [
      {
        c: `no-creep`,
        label: CREEPINESS_LABELS[0],
        value: values[0],
        offset: 0,
      },
      {
        c: `little-creep`,
        label: CREEPINESS_LABELS[1],
        value: values[1],
        offset: 225,
      },
      {
        c: `somewhat-creep`,
        label: CREEPINESS_LABELS[2],
        value: values[2],
        offset: 475,
      },
      {
        c: `very-creep`,
        label: CREEPINESS_LABELS[3],
        value: values[3],
        offset: 725,
      },
      {
        c: `super-creep`,
        label: CREEPINESS_LABELS[4],
        value: values[4],
        offset: 975,
      },
    ];
    let sum = data.reduce((tally, v) => tally + v.value, 0);

    return {
      totalCreepiness: sum < 1 ? 1 : sum,
      creepinessData: data,
    };
  }

  render() {
    return (
      <React.Fragment>
        <table id="creepiness-score" className="w-100">
          <tbody>
            {this.state.creepinessData.map((data, index) => {
              let percent = Math.round(
                (100 * data.value) / this.state.totalCreepiness
              );
              let voteColumn =
                this.props.userVoteGroup === index ? `your-vote` : ``;

              return (
                <tr key={data.c} className={`${voteColumn} ${data.c}`}>
                  <th>
                    <div className="bar" style={{ height: `${percent}px` }} />
                    <span className="creep-label">{data.label}</span>
                    <span className="creep-face" />
                  </th>
                  <td className="creepiness">{percent}%</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="d-flex justify-content-between">
          <div className="text-muted">Not creepy</div>
          <div className="text-muted">Super creepy</div>
        </div>
      </React.Fragment>
    );
  }
}
