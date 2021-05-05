import { Component } from "react";
import classNames from "classnames";

/**
 * Renders a special style input box for petition form.
 */
class FloatingLabelInput extends Component {
  render() {
    let className = classNames(`form-label-group`, this.props.className);

    return (
      <div className={className}>
        <input
          className="form-control"
          disabled={this.props.disabled}
          ref={(element) => {
            this.element = element;
          }}
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

export default FloatingLabelInput;
