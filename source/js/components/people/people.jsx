import React from 'react';
import Person from './person.jsx';

export default class People extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      people: []
    };
  }

  componentDidMount() {
    let networkSiteUrl = this.props.env.NETWORK_SITE_URL;

    // HEROKU_APP_DOMAIN is used by review apps
    if (!networkSiteUrl && this.props.env.HEROKU_APP_NAME) {
      networkSiteUrl = `https://${this.props.env.HEROKU_APP_NAME}.herokuapp.com`;
    }

    let xhr = new XMLHttpRequest();

    xhr.addEventListener(`load`, () => {
      this.setState({
        people: JSON.parse(xhr.response)
      }, () => {
        this.props.whenLoaded();
      });
    });

    xhr.open(`GET`, `${networkSiteUrl}/api/people/?format=json&featured=True&page=1`);
    xhr.send();
  }

  render() {
    let people = this.state.people.map((person, index) => {
      return (
        <Person key={index} metadata={person}/>
      );
    });

    return (
      <div className="row">
        {people}
      </div>
    );
  }
}
