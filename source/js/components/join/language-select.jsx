import React from "react";

export default class LanguageSelect extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: "" };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
    console.log(`After: ${this.state.value}`);
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
    let meta_lang = document
      .querySelector(`meta[property="wagtail:language"]`)
      .getAttribute("content");
    let value = this.state.value;
    let classes = this.props.className;

    return (
      <select value={value ? value : meta_lang} onChange={this.handleChange} className={classes}>
        {this.renderOptions()}
      </select>
    );
  }
}
