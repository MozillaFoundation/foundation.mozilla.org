// TODO: Inject likely % in .bar and .likelyhood-words

import React from "react";
import { Localized } from "../../../components/localized.js";

export default class LikelyhoodChart extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let values = this.props.values;
    let total = values[0] + values[1];
    let perc = 50;

    if (total > 0) {
      perc = Math.round((100 * values[0]) / total, 10);
    }

    let likely = (
      <Localized stringId="percent-likely-to-buy" vars={{ perc: 100 - perc }}>
        {`{$perc}% likely to buy it`}
      </Localized>
    );
    let unlikely = (
      <Localized stringId="percent-not-likely-to-buy" vars={{ perc }}>
        {`{$perc}% not likely to buy it`}
      </Localized>
    );

    if (this.props.isSoftware) {
      likely = (
        <Localized stringId="percent-likely-to-use" vars={{ perc: 100 - perc }}>
          {`{$perc}% likely to use it`}
        </Localized>
      );
      unlikely = (
        <Localized stringId="percent-not-likely-to-use" vars={{ perc }}>
          {`{$perc}% not likely to use it`}
        </Localized>
      );
    }

    return (
      <div>
        <table id="likelyhood-score">
          <tbody>
            <tr className="likely">
              <th>
                <span className="likely-label">
                  <Localized stringId="likely">{`Likely`}</Localized>
                </span>
              </th>
              <td className="likelyhood">
                <span className="bar" style={{ width: `${100 - perc}%` }} />
                <span className="likelyhood-words">{likely}</span>
              </td>
            </tr>
            <tr className="unlikely">
              <th>
                <span className="likely-label">
                  <Localized stringId="not-likely">{`Not likely`}</Localized>
                </span>
              </th>
              <td className="likelyhood">
                <span className="bar" style={{ width: `${perc}%` }} />
                <span className="likelyhood-words">{unlikely}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  }
}
