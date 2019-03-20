var modernBrowser = (
  'fetch' in window &&
  'assign' in Object
);

if ( !modernBrowser ) {
  var scriptElement = document.createElement('script');

  scriptElement.async = false;
  scriptElement.src = '/_js/polyfills.compiled.js';
  document.head.appendChild(scriptElement);
}
