import React from 'react';

export default class PulseProjectList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  fetchProjects(tag) {
    let projectXHR = new XMLHttpRequest();

    projectXHR.addEventListener(`load`, () => {
      console.log(JSON.parse(projectXHR.response));
    });

    projectXHR.open(`GET`, `https://${this.props.env.PULSE_API_DOMAIN}/api/pulse/entries/?format=json&tag=${tag}`);
    projectXHR.send();
  }

  componentDidMount() {
    let tag = this.props.tags; // TODO: Allow multiple tags - may require pulse API refactor

    this.fetchProjects(tag);
  }

  render() {
    return (
      <div>Hello</div>
    );
  }
}
