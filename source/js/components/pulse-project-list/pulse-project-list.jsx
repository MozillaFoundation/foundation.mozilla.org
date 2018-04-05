import React from 'react';
import PropTypes from 'prop-types';

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

    projectXHR.open(`GET`, `https://${this.props.env.PULSE_API_DOMAIN}/api/pulse/v2/entries/?format=json&search=${query}${this.props.featured ? `&featured=True` : ``}`);
    projectXHR.send();
  }

  componentDidMount() {
    this.fetchProjects(this.props.query);
  }

  render() {
    let projectList = this.state.projects.map((project, index) => {

      let byline = null;

      if (project.related_creators.length) {
        byline = `By ${project.related_creators.map(rc => rc.name).join(`, `)}`;
      }

      return (
        <div className="col-sm-12 col-md-4 my-4" key={`pulse-project-${index}`}>
          <a className="pulse-project" href={`https://${this.props.env.PULSE_DOMAIN}/entry/${project.id}`}>
            <div className="thumbnail">
              <div className="img-container">
                <img className={`project-image${ project.thumbnail ? `` : ` placeholder` }`} src={ project.thumbnail ? project.thumbnail : `/_images/proportional-spacer.png` }/>
              </div>
            </div>
            <h5 className="project-title h5-heading my-2">{project.title}</h5>
          </a>
          { byline && <p className="small-gray my-1">{byline}</p> }
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
  query: PropTypes.string.isRequired,
  max: PropTypes.number,
  reverseChronological: PropTypes.bool,
  featured: PropTypes.bool
};

PulseProjectList.defaultProps = {
  max: null,
  reverseChronological: true,
  featured: false
};
