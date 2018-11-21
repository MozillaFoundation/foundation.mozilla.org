export default {
  initialize: function() {
    var _dntStatus = navigator.doNotTrack || navigator.msDoNotTrack;
    var fxMatch = navigator.userAgent.match(/Firefox\/(\d+)/);
    var ie10Match = navigator.userAgent.match(/MSIE 10/i);
    var w8Match = navigator.appVersion.match(/Windows NT 6.2/);

    if (fxMatch && Number(fxMatch[1]) < 32) {
      _dntStatus = 'Unspecified';
    } else if (ie10Match && w8Match) {
      _dntStatus = 'Unspecified';
    } else {
      _dntStatus = { '0': 'Disabled', '1': 'Enabled' }[_dntStatus] || 'Unspecified';
    }

    if (_dntStatus !== 'Enabled'){
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-87658599-6', 'auto');
      ga('send', 'pageview');
    }
  },

  sendGAEvent(category = ``, action = ``, label = ``) {
    if (!window.ga) {
      return;
    }
    window.ga('send', category, 'navigation', action, label);
    window.ga('send', 'event', 'navigation', 'page footer cta', document.querySelectorAll('.cms h1').length > 0 ? document.querySelectorAll('.cms h1')[0].innerText + ' - footer cta' : '');
  }
};
