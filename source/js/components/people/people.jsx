import React from 'react';
import Person from './person.jsx';
import env from '../../../../env.json';

let networkApiDomain = env.NETWORK_API_DOMAIN

// HEROKU_APP_DOMAIN is used by review apps
if (!networkApiDomain && env.HEROKU_APP_NAME) {
  networkApiDomain = `${env.HEROKU_APP_NAME}.herokuapp.com`
}

export default class People extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      people: []
    };
  }

  componentDidMount() {
    let xhr = new XMLHttpRequest();

    xhr.addEventListener(`load`, () => {
      this.setState({
        people: JSON.parse(xhr.response)
      });
    });

    xhr.open(`GET`, `https://${env.networkApiDomain}/api/people/?format=json&featured=True&page=1`);
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
