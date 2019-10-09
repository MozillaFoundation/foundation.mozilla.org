import React from "react";
import classNames from "classnames";
import { getCurrentLanguage } from "../petition/locales";

export default class LanguageSelect extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: "" };
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  renderOptions() {
    let languages = {
      en: `English`,
      de: `Deutsch`,
      es: `Español`,
      fr: `Français`,
      pl: `Polski`,
      pt: `Português`
    };

    let lang_codes = Object.keys(languages);
    let options = lang_codes.map(lang_code => {
      return (
        <option key={lang_code} value={lang_code}>
          {languages[lang_code]}
        </option>
      );
    });

    return options;
  }

  render() {
    let meta_lang = getCurrentLanguage();
    let classes = classNames(`form-control`, this.props.className);

    return (
      <select
        value={this.state.value || meta_lang}
        onChange={evt => this.handleChange(evt)}
        className={classes}
      >
        {this.renderOptions()}
      </select>
    );
  }
}
