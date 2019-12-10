import React from "react";
import classNames from "classnames";
import { i18n } from "../i18n/catalogs-loader.jsx";
import { t } from "@lingui/macro";

export default class LanguageSelect extends React.Component {
  constructor(props) {
    super(props);
  }

  handleChange(event) {
    this.props.handleLangChange(event.target.value);
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
    let classes = classNames(`form-control`, this.props.className);

    return (
      <select
        value={this.props.selectedLang}
        onChange={evt => this.handleChange(evt)}
        className={classes}
        id={`userLanguage-${this.props.formPosition}`}
        aria-label={i18n._(t`Please select your preferred language`)}
      >
        {this.renderOptions()}
      </select>
    );
  }
}
