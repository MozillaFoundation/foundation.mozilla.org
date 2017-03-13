import React from 'react';
import Person from './person.jsx';
import peopleData from '../../../json/temp/people.json';

export default class People extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let people = peopleData.map((person, index) => {
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
