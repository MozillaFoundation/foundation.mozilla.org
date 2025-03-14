/**
 * Signing users up for the Foundation newsletter using the Basket client.
 * https://basket.readthedocs.io/
 */

// TODO: make this dynamic based on env. Staging is allizom.org. https://github.com/mozilla/network/issues/118
var url = `https://www.mozilla.org/en-US/newsletter/`;

var basketSignup = function (transaction, onSuccessCallback, onFailCallback) {
  var payload = {
    format: `H`, // HTML emails
    newsletter: transaction.newsletter,
    triggerWelcome: `N`,
    email: transaction.email,
    privacy: transaction.privacy || false,
  };

  var errorArray = [];
  var newsletterErrors = [];

  while (newsletterErrors.firstChild) {
    newsletterErrors.removeChild(newsletterErrors.firstChild);
  }

  var params =
    `email=` +
    encodeURIComponent(payload.email) +
    `&newsletters=` +
    payload.newsletter +
    `&privacy=` +
    payload.privacy +
    `&fmt=` +
    payload.format +
    `&source_url=` +
    encodeURIComponent(document.location.href);

  var xhr = new XMLHttpRequest();

  xhr.onload = function (r) {
    if (r.target.status >= 200 && r.target.status < 300) {
      var response = r.target.response;

      if (response === null) {
        onFailCallback(new Error());
        return;
      }

      if (response.success === true) {
        onSuccessCallback();
      } else {
        if (response.errors) {
          for (var i = 0; i < response.errors.length; i++) {
            errorArray.push(response.errors[i]);
          }
        }
        onFailCallback(new Error(errorArray));
      }
    } else {
      onFailCallback(new Error());
    }
  };

  xhr.onerror = function (e) {
    onFailCallback(e);
  };

  xhr.open(`POST`, url, true);
  xhr.setRequestHeader(`Content-type`, `application/x-www-form-urlencoded`);
  xhr.setRequestHeader(`X-Requested-With`, `XMLHttpRequest`);
  xhr.timeout = 5000;
  xhr.ontimeout = onFailCallback;
  xhr.responseType = `json`;
  xhr.send(params);

  return false;
};

module.exports = basketSignup;
