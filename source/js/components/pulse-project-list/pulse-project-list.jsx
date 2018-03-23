import React from 'react';

export default class PulseProjectList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      projects: []
    };
  }

  fetchProjects(query) {
    let projectXHR = new XMLHttpRequest();

    projectXHR.addEventListener(`load`, () => {
      let projects = JSON.parse(projectXHR.response);

      this.setState({
        projects: projects.results.slice(0, this.props.max || 6)
      });
    });

    projectXHR.open(`GET`, `https://${this.props.env.PULSE_API_DOMAIN}/api/pulse/entries/?format=json&search=${query}`);
    projectXHR.send();
  }

  componentDidMount() {
    this.fetchProjects(this.props.query);
  }

  render() {
    let projectList = this.state.projects.map((project, index) => {
      return (
        <div className="col-sm-12 col-md-4 mb-4 mb-md-0" key={`pulse-project-${index}`}>
          <a className="pulse-project" href={`https://${this.props.env.PULSE_DOMAIN}/entry/${project.id}`}>
            <img className="project-image" src={project.thumbnail} />
            <h5 className="h5-black my-2">{project.title}</h5>
          </a>
          <p className="small-gray my-1">By Zannah Marsh, Abigail Cabunoc Mayes, Rizwan Tufail, Chad Sansing</p>
        </div>
      );
    });

    return (
      <div className="row">{projectList}</div>
    );
  }
}
