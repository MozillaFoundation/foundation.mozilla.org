import React from "react";
import ReactDOM from "react-dom";
import News from "../../components/news/news.jsx";

/**
 * Inject news items to News page
 * @param {Array} apps The existing array we are using to to track all ReactDOM.render calls
 * @param {Object} env Object of environment variables
 */
export default (apps, env) => {
  if (document.querySelector(`#view-news #news`)) {
    apps.push(
      new Promise((resolve) => {
        ReactDOM.render(
          <News env={env} whenLoaded={() => resolve()} />,
          document.querySelector(`#news`)
        );
      })
    );
  }
};
