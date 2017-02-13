import React from 'react';

export default class Person extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="col-lg-3 p-3 person">
        <h4>{this.props.metadata.name}</h4>
        <p>👤 {this.props.metadata.role}</p>
        <p>▼ {this.props.metadata.location}</p>
        <p>&hearts;&nbsp;<small>{this.props.metadata.teams[0]}</small></p>
      </div>
    );
  }
}
