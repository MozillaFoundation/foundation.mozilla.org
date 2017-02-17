import React from 'react';

export default class PulseProjects extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let projects = this.props.projects.map((project, index) => {
      return (
        <div key={index} className="col-sm-4 mb-3 p-3">
          <img className="mb-3" src={project.thumbnail_url} />
          <p className="h4-medium-black">{project.title}</p>
          <p className="small-gray">{`By ${project.creators.join(`, `)}`}</p>
          <p className="body-black">{project.description}</p>
          <a className="cta-link" href={project.content_url}>Read More</a>
        </div>
      );
    });

    return (
      <div className="row mb-5">
        {projects}
      </div>
    );
  }
}
