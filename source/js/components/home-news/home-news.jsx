import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

export default class HomeNews extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  render() {
    let newsItem = (item, featured=false, index=null, hr=false) => {
      return (
        <div className="news-item" key={index}>
          <div className="d-flex align-items-center mb-2">
            { item.glyph && <img src={item.glyph} className="mr-2 glyph"/> }
            <p className="h6-heading-uppercase mb-0">{item.outlet}</p>
          </div>
          <h5 className="mb-2">
            <a href={item.link} className={featured ? `h4-heading` : `h5-heading`}>{item.headline}</a>
          </h5>
          <p className="h6-heading mb-2">{ item.author && `by ${item.author} on ` }{ moment(item.date, `YYYY-MM-DD`).format(`MMMM YYYY`) }</p>
          { item.excerpt && <p>{item.excerpt}</p> }
          { hr && <hr/> }
        </div>
      );

    };

    let unfeaturedNews = this.props.data.slice(1).map((item, index, array) => {
      return newsItem(item, false, index, index < array.length - 1);
    });

    let featuredNews = this.props.data[0];

    return (
      <div className="row mb-3">
        <div className="col-md-6 mb-0 pb-4">
          <div className="play-button-wrapper">
            <img src={featuredNews.thumbnail}/>
            { featuredNews.is_video && <a href={featuredNews.link} className="play-button-overlay"></a> }
          </div>
          <div className="row">
            <div className="col-12">
              <div className="key-item mx-2 mx-md-4 p-3">
                { newsItem(featuredNews, true) }
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-6 mb-0 pb-4">{ unfeaturedNews }</div>
      </div>
    );
  }
}

HomeNews.propTypes = {
  data: PropTypes.array
};

HomeNews.defaultProps = {
  data: []
};
