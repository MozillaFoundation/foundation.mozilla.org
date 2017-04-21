import React from 'react';
import peopleData from '../../../json/temp/people.json';

const featuredPeople = peopleData.filter(person => person.featured);

export default class People extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let people = featuredPeople.slice(0,4).map((person, index) => {
      let filteredLinks = {};

      // Django returns empty strings instead of null for empty links, so let's filter empty links out:
      for(let key in person.links) {
        if (Object.prototype.hasOwnProperty.call(person.links, key)) {
          if (!!person.links[key] !== ``) {
            filteredLinks[key] = person.links[key];
          }
        }
      }

      let socialLinks = Object.keys(filteredLinks).map((linkKey, i) => {
        let classes = `${linkKey} gray small mr-4`;

        return (
          <a href={person.links[linkKey]} className={classes} key={i}></a>
        );
      });

      return (
        <div className="col-sm-6 col-md-3" key={index}>
          <img src={person.image} className="img-fluid d-block" alt="Headshot" />
          <h2 className="h5-black my-2">{person.name}</h2>
          <p className="small-gray">{person.affiliations.join(`, `)}</p>
          <div className="person-social-links mt-3">
            {socialLinks}
          </div>
        </div>
      );
    });

    return (
      <div className="row mb-5">
        {people}
      </div>
    );
  }
}
