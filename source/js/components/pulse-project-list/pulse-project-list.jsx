import React from 'react';
import PropTypes from 'prop-types';

export default class PulseProjectList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      projects: []
    };
  }

  fetchProjects() {
    let projectXHR = new XMLHttpRequest();

    projectXHR.addEventListener(`load`, () => {
      let projects = JSON.parse(projectXHR.response);

      projects.results = projects.results.sort((a,b) => {
        if (this.props.reverseChronological) {
          return Date.parse(a.created) < Date.parse(b.created) ? 1 : -1;
        } else {
          return Date.parse(a.created) > Date.parse(b.created) ? 1 : -1;
        }
      });

      this.setState({
        projects: this.props.max ? projects.results.slice(0, this.props.max) : projects.results
      });
    });

    const apiURL = `${this.props.env.PULSE_API_DOMAIN}/api/pulse/v2/entries/`;

    const params = {
      "format": `json`,
      "help_type": this.props.help && this.props.help !== `all` ? this.props.help : null,
      "issue": this.props.issues && this.props.issues !== `all` ? this.props.issues : null,
      "page_size": this.props.max ? this.props.max : 12,
      "search": this.props.query,
      "featured": this.props.featured && `True`
    };

    // Serialize parameters into a query string
    const serializedParams = Object.keys(params).filter((key) => params[key]).map((key) => {
      return `${key}=${encodeURIComponent(params[key])}`;
    });

    const apiURLwithQuery = `${apiURL}?${serializedParams.join(`&`)}`;

    projectXHR.open(`GET`, apiURLwithQuery);
    projectXHR.send();
  }

  componentDidMount() {
    this.fetchProjects();
  }

  render() {
    let projectList = this.state.projects.map((project, index) => {

      let byline = null;

      if (project.related_creators.length) {
        byline = `By ${project.related_creators.map(rc => rc.name).join(`, `)}`;
      }

      return (
        <div className="col-6 col-md-4 my-4" key={`pulse-project-${index}`}>
          <a className="pulse-project" href={`https://${this.props.env.PULSE_DOMAIN}/entry/${project.id}`} target="_blank" rel="noopener noreferrer">
            <div className="thumbnail">
              <div className="img-container">
                <img className={`project-image${ project.thumbnail ? `` : ` placeholder` }`} src={ project.thumbnail ? project.thumbnail : `/_images/proportional-spacer.png` }/>
              </div>
            </div>
            <h5 className="project-title h5-heading my-2">{project.title}</h5>
          </a>
          { byline && <p className="h6-heading my-1">{byline}</p> }
        </div>
      );
    });

    return (
      <div className="row">{projectList}</div>
    );
  }
}

PulseProjectList.propTypes = {
  env: PropTypes.object.isRequired,
  featured: PropTypes.bool,
  help: PropTypes.string,
  issues: PropTypes.string,
  max: PropTypes.number,
  query: PropTypes.string.isRequired,
  reverseChronological: PropTypes.bool
};
