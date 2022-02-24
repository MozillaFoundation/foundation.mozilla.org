import { Component } from "react";
import PropTypes from "prop-types";
import moment from "moment";
import { getCurrentLanguage } from "../petition/locales";

/**
 * Pulls news items from API and
 * renders them into a list categorized by year.
 */
class News extends Component {
  constructor(props) {
    super(props);

    this.state = {
      news: [],
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
      this.setState(
        {
          news: JSON.parse(xhr.response),
        },
        () => {
          if (this.props.whenLoaded) {
            this.props.whenLoaded();
          }
        }
      );
    });

    xhr.open(
      `GET`,
      `${networkSiteUrl}/api/news/?format=json&featured=True&page=1`
    );
    xhr.send();
  }

  render() {
    const currentLanguage = getCurrentLanguage();

    let blurb = (newsItem, hasHR = true) => {
      let formattedPublishDate  = new Date(newsItem.date).toLocaleDateString(
        currentLanguage|| `en-US`,
        {
          month: "long",
          year: "numeric",
        }
      );

      return (
        <div key={newsItem.headline}>
          <div className="mb-3 news-item">
            <div className="d-flex align-items-center mb-2">
              <p className="h6-heading mb-0">{newsItem.outlet}</p>
            </div>
            <h3 className="h3-heading mb-2">
              <a href={newsItem.link} className="newsItem headline">
                {newsItem.headline}
              </a>
            </h3>
            <p className="h6-heading">
              {newsItem.author && <span>by {newsItem.author} on </span>}
              {formattedPublishDate}
            </p>
          </div>
          {hasHR && <hr />}
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
            <h2 className="type-accent">{year}</h2>
          </div>
          <div className="col-md-8 col-lg-7">
            {filteredNews.map((item, index, array) => {
              return blurb(item, index < array.length - 1);
            })}
          </div>
        </div>
      );
    };

    const startYear = 2016;
    const currentYear = new Date().getFullYear();

    let year = startYear;
    let newsByYear = [];

    while (year <= currentYear) {
      newsByYear.unshift(newsForYear(year));
      year++;
    }

    return <div className="container py-5">{newsByYear}</div>;
  }
}

News.propTypes = {
  data: PropTypes.array,
};

News.defaultProps = {
  data: [],
};

export default News;
