let _dntStatus = navigator.doNotTrack || navigator.msDoNotTrack,
    fxMatch = navigator.userAgent.match(/Firefox\/(\d+)/),
    ie10Match = navigator.userAgent.match(/MSIE 10/i),
    w8Match = navigator.appVersion.match(/Windows NT 6.2/);

if (fxMatch && Number(fxMatch[1]) < 32) {
  _dntStatus = `Unspecified`;
} else if (ie10Match && w8Match) {
  _dntStatus = `Unspecified`;
} else {
  _dntStatus = { '0': `Disabled`, '1': `Enabled` }[_dntStatus] || `Unspecified`;
}

const DNT = {
  allowTracking: (_dntStatus !== `Enabled`)
};

export default DNT;
