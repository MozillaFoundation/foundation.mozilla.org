import React from 'react';
import PropTypes from 'prop-types';
import FellowList from './fellow-list.jsx';

export default class SingleFilterFellowList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedOption: this.props.selectedOption
    };
  }

  generateQuery() {
    let query = {};

    query[this.props.filterType] = this.state.selectedOption;

    return query;
  }

  handleFilterClick(option) {
    if (option !== this.state.selectedOption) {
      this.setState({
        selectedOption: option
      });
    }
  }

  renderFilters() {
    return <div className="fellowships-directory-filter px-2">
      { this.props.filterOptions.map(option => {
        let id = `fellow-list-${this.props.filterType}-${option.replace(` `, `-`)}`;

        return <div key={option} className="filter-option">
          <input type="radio"
            name={this.props.filterType}
            value={option}
            id={id}
            onClick={() => this.handleFilterClick(option)}
            defaultChecked={this.state.selectedOption === option}
          />
          <label htmlFor={id}>{option}</label>
        </div>;
      })
      }
    </div>;
  }

  render() {
    return (
      <div>
        <div className="row">
          <div className="col-12 mb-5">
            {this.renderFilters()}
          </div>
        </div>
        <FellowList env={this.props.env} query={this.generateQuery()} />
      </div>
    );
  }
}

SingleFilterFellowList.propTypes = {
  env: PropTypes.object.isRequired,
  filterType: PropTypes.string.isRequired,
  filterOptions: PropTypes.array.isRequired,
  selectedOption: PropTypes.string.isRequired
};
