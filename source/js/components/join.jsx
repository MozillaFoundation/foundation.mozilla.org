import React from 'react';

export default class JoinUs extends React.Component {
  show () {
    console.log(`show`);

    this.setState({
      isHidden: false
    });
  }

  hide () {
    console.log(`hide`);

    this.setState({
      isHidden: true
    });
  }

  constructor(props) {
    super(props);

    this.state = {
      isHidden: true
    };
  }

  render() {
    return (
      <div style={{background: `#eee`}} hidden={this.state.isHidden} className="row py-5">
        <div className="col-6">
          <h3 className="h3-cta-black">Join Our Ranks</h3>
          <p className="body-black">Access to bright minds, passionate community, and invaluable resources.</p>
        </div>
        <div className="col-6">
          <form>
            <input placeholder="Email Address"/>
            <button className="btn btn-normal">Join Us</button>
            <label>
              <input type="checkbox"/><span className="small-gray">&nbsp;I'm okay with Mozilla handling my info as explained in this <a href="#TODO">Privacy Notice</a></span>
            </label>
          </form>
        </div>
      </div>
    );
  }
}
