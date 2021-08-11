import { Component } from "react";
import classNames from "classnames";

/**
 * Displays a language list dropdown for newsletter sign-up form.
 */
class JoinUsLanguageSelect extends Component {
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
      "pt-BR": `Português`,
    };

    let lang_codes = Object.keys(languages);
    let options = lang_codes.map((lang_code) => {
      const optionAttributes = {
        key: lang_code,
        value: lang_code,
      };
      return <option {...optionAttributes}>{languages[lang_code]}</option>;
    });

    return options;
  }

  render() {
    let classes = classNames(`form-control`, this.props.className);

    return (
      <select
        className={classes}
        id={`userLanguage-${this.props.formPosition}`}
        value={this.props.selectedLang}
        onBlur={(evt) => this.handleChange(evt)}
        onChange={(evt) => this.handleChange(evt)}
        aria-label="Please select your preferred language"
      >
        {this.renderOptions()}
      </select>
    );
  }
}

export default JoinUsLanguageSelect;
