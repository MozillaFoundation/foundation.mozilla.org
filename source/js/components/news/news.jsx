import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

export default class News extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      news: []
    };
  }

  componentDidMount() {
    let networkSiteUrl = this.props.env.NETWORK_SITE_URL;

    // HEROKU_APP_DOMAIN is used by review apps
    if (!networkSiteUrl && this.props.env.HEROKU_APP_NAME) {
      networkSiteUrl = `https://${this.props.env.HEROKU_APP_NAME}.herokuapp.com`;
    }

    let xhr = new XMLHttpRequest();

    xhr.addEventListener(`load`, () => {
      this.setState({
        news: JSON.parse(xhr.response)
      });
    });

    xhr.open(`GET`, `${networkSiteUrl}/api/news/?format=json&featured=True&page=1`);
    xhr.send();
  }

  render() {
    let blurb = (newsItem, hasHR=true) => {
      return (
        <div key={newsItem.headline}>
          <div className="mb-3 news-item">
            <div className="d-flex align-items-center mb-3">
              { newsItem.glyph && <img src={newsItem.glyph} className="mr-2 glyph"/> }
              <p className="h6-gray mb-0">{newsItem.outlet}</p>
            </div>
            <h3 className="h4-medium-black mb-2">
              <a href={newsItem.link} className="newsItem headline">{newsItem.headline}</a>
            </h3>
            { newsItem.author && <p className="italic-black">by {newsItem.author}</p> }
            <p className="small-gray">{moment(newsItem.date, `YYYY-MM-DD`).format(`MMMM YYYY`)}</p>
          </div>
          { hasHR && <hr/> }
        </div>
      );
    };

    let newsForYear = (year) => {
      let filteredNews = this.state.news.filter((item) => {
        return item.date.match(year);
      });

      return (
        <div className="row mb-5" key={year}>
          <div className="col-md-4 d-md-flex justify-content-end">
            <h2 className="h2-typeaccent">{year}</h2>
          </div>
          <div className="col-md-8 col-lg-7">
            { filteredNews.map((item, index, array) => { return blurb(item, index < array.length - 1); }) }
          </div>
        </div>
      );
    };

    const startYear = 2016;
    const currentYear = moment().year();

    let year = startYear;
    let newsByYear = [];

    while (year <= currentYear) {
      newsByYear.unshift(newsForYear(year));
      year++;
    }

    return (
      <div className="container py-5">
        { newsByYear }
      </div>
    );
  }
}

News.propTypes = {
  data: PropTypes.array
};

News.defaultProps = {
  data: []
};
