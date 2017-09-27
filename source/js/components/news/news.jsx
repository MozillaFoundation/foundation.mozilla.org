import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import env from '../../../../env.json';

let networkApiDomain = env.NETWORK_API_DOMAIN || env.HEROKU_APP_NAME

export default class News extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      news: []
    };
  }

  componentDidMount() {
    let xhr = new XMLHttpRequest();

    xhr.addEventListener(`load`, () => {
      this.setState({
        news: JSON.parse(xhr.response)
      });
    });

    xhr.open(`GET`, `https://${networkApiDomain}/api/news/?format=json&featured=True&page=1`);
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
            <h2 className="h2-typeaccents-gray">{year}</h2>
          </div>
          <div className="col-md-8 col-lg-7">
            { filteredNews.map((item, index, array) => { return blurb(item, index < array.length - 1); }) }
          </div>
        </div>
      );
    };

    return (
      <div className="container py-5">
        { newsForYear(2017) }
        { newsForYear(2016) }
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
