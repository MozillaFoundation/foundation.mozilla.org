import { Component } from "react";
import PropTypes from "prop-types";

/**
 * Pulls Pulse projects from Pulse API and
 * renders it as a list.
 */
class PulseProjectList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      projects: [],
    };
  }

  fetchProjects() {
    let projectXHR = new XMLHttpRequest();

    projectXHR.addEventListener(`load`, () => {
      let projects = JSON.parse(projectXHR.response);

      this.setState(
        {
          projects: this.props.max
            ? projects.results.slice(0, this.props.max)
            : projects.results,
        },
        () => {
          if (this.props.whenLoaded) {
            this.props.whenLoaded();
          }
        }
      );
    });

    const apiURL = `${this.props.env.PULSE_API_DOMAIN}/api/pulse/v2/entries/`;

    const params = {
      format: `json`,
      help_type:
        this.props.help && this.props.help !== `all` ? this.props.help : null,
      issue:
        this.props.issues && this.props.issues !== `all`
          ? this.props.issues
          : null,
      page_size: this.props.max ? this.props.max : 12,
      search: this.props.query,
      featured: this.props.featured && `True`,
      ordering: this.props.reverseChronological ? `-created` : `created`,
    };

    // Serialize parameters into a query string
    const serializedParams = Object.keys(params)
      .filter((key) => params[key])
      .map((key) => {
        return `${key}=${encodeURIComponent(params[key])}`;
      });

    const apiURLwithQuery = `${apiURL}?${serializedParams.join(`&`)}`;

    projectXHR.open(`GET`, apiURLwithQuery);
    projectXHR.send();
  }

  // Giving users ability to link to pulse objects using an anchor link
  // and having it render in the right place after recieving data.
  scrollToLinkedPulseObject(){
    const linkedPulseObject = document.querySelector(window.location.hash);
    linkedPulseObject?.scrollIntoView()
  }

  componentDidMount() {
    this.fetchProjects();
  }

  componentDidUpdate() {
    if(window.location.hash){
      this.scrollToLinkedPulseObject()
    }
  }

  render() {
    let projectList = this.state.projects.map((project, index) => {
      let byline = null;
      let url;

      if (project.related_creators.length) {
        byline = `By ${project.related_creators
          .map((rc) => rc.name)
          .join(`, `)}`;
      }

      if (this.props.directLink) {
        url = project.content_url;
      } else {
        url = `${this.props.env.PULSE_DOMAIN}/entry/${project.id}`;
      }

      return (
        <div
          className="pulse-project-wrapper col-6 col-md-4 my-4 d-print-inline-block"
          key={`pulse-project-${index}`}
        >
          <a
            className="pulse-project"
            href={url}
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className="thumbnail">
              <div className="img-container">
                <img
                  className={`project-image${
                    project.thumbnail ? `` : ` placeholder`
                  }`}
                  src={
                    project.thumbnail
                      ? project.thumbnail
                      : `/static/_images/proportional-spacer.png`
                  }
                  alt=""
                />
              </div>
            </div>
            <h5 className="project-title h5-heading my-2">{project.title}</h5>
          </a>
          {byline && <p className="body-small my-1">{byline}</p>}
        </div>
      );
    });

    return <div className="row">{projectList}</div>;
  }
}

PulseProjectList.propTypes = {
  env: PropTypes.object.isRequired,
  featured: PropTypes.bool,
  directLink: PropTypes.bool,
  help: PropTypes.string,
  issues: PropTypes.string,
  max: PropTypes.number,
  query: PropTypes.string.isRequired,
  reverseChronological: PropTypes.bool,
};

export default PulseProjectList;
