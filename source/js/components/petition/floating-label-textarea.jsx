import React from 'react';
import classNames from 'classnames';

export default class FloatingLabelInput extends React.Component {
  render() {
    let className = classNames(`form-label-group`, this.props.className);

    return (
      <div className={className}>
        <textarea className="form-control"
          disabled={this.props.disabled}
          ref={(element) => { this.element = element; }}
          id={this.props.id}
          type={this.props.type}
          placeholder={this.props.label}
          onFocus={this.props.onFocus}
        />
        <label htmlFor={this.props.id}>{this.props.label}</label>
      </div>
    );
  }
}
