import { Component } from "react";
import classNames from "classnames";

/**
 * Renders a special style textarea box for petition form.
 */
class FloatingLabelTextarea extends Component {
  render() {
    let className = classNames(`form-label-group`, this.props.className);

    return (
      <div className={className}>
        <textarea
          className="tw-form-control has-error:tw-border has-error:tw-border-solid has-error:tw-border-[#c01] dark:has-error:tw-border-2 dark:has-error:tw-border-red-40"
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

export default FloatingLabelTextarea;
