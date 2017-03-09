var url = process.env.SIGNUP;
url = `https://basket-dev.allizom.org/news/subscribe/`;

var basketSignup = function(transaction, onSuccessCallback, onFailCallback) {
  console.log(url);
  var payload = {
    format: `html`,
    newsletter: `mozilla-leadership-network`,
    triggerWelcome: `N`,
    email: `success@example.com`,
    privacy: true || false
  };

  console.log(payload);

  var errorArray = [];
  var newsletterErrors = [];

  errorArray = [];
  while (newsletterErrors.firstChild) { newsletterErrors.removeChild(newsletterErrors.firstChild); }

  var params = `email=` + encodeURIComponent(payload.email) +
                  `&newsletters=` + payload.newsletter +
                   `&privacy=`+ payload.privacy +
                  `&fmt=` + payload.format +
                  `&source_url=` + encodeURIComponent(document.location.href);
  console.log(params);

  var xhr = new XMLHttpRequest();

  xhr.onload = function(r) {
    console.log(`onload`);
    console.log(r);
    if (r.target.status >= 200 && r.target.status < 300) {
      var response = r.target.response;

      if(response === null ) {
        onFailCallback(new Error());
        return;
      }

      if (response.success === true) {
        onSuccessCallback();
      } else {
        if(response.errors) {
          for (var i = 0; i < response.errors.length; i++) {
            errorArray.push(response.errors[i]);
          }
        }
        onFailCallback(new Error());
      }
    } else {
      onFailCallback(new Error());
    }
  };

  xhr.onerror = function(e) {
    console.log(`onerror`);
    onFailCallback(e);
  };

  xhr.open(`POST`, url, true);
  xhr.setRequestHeader(`Content-type`, `application/x-www-form-urlencoded`);
  xhr.setRequestHeader(`X-Requested-With`,`XMLHttpRequest`);
  xhr.timeout = 5000;
  xhr.ontimeout = onFailCallback;
  xhr.responseType = `json`;
  xhr.send(params);

  return false;

};

module.exports = basketSignup;
