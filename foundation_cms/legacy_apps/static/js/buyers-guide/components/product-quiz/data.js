const IMG_DIR = "/static/legacy_apps/_images/buyers-guide/consumer-creepometer";

export const POINTS = {
  good: 0,
  soso: 1,
  bad: 2,
};

export const PRODUCTS = {
  Signal: {
    name: "Signal",
    company: "Signal Foundation",
    imgSrc: `${IMG_DIR}/products/Signal.png`,
    points: POINTS.good,
  },
  "SL Speakers": {
    name: "SL Speakers",
    company: "Sonos",
    imgSrc: `${IMG_DIR}/products/Sonos_SL_Speakers.png`,
    points: POINTS.good,
  },
  "Garmin Fenix": {
    name: "Garmin Fenix",
    company: "Garmin",
    imgSrc: `${IMG_DIR}/products/Garmin_Fenix.png`,
    points: POINTS.good,
  },
  "Nintendo Switch": {
    name: "Nintendo Switch",
    company: "Nintendo",
    imgSrc: `${IMG_DIR}/products/Nintendo_Switch.png`,
    points: POINTS.good,
  },
  "Nvidia Shield TV": {
    name: "Nvidia Shield TV",
    company: "Nvidia",
    imgSrc: `${IMG_DIR}/products/Nvidia_Shield_TV.png`,
    points: POINTS.good,
  },
  "Apple Watch": {
    name: "Apple Watch",
    company: "Apple",
    imgSrc: `${IMG_DIR}/products/Apple_Watch.png`,
    points: POINTS.soso,
  },
  Telegram: {
    name: "Telegram",
    company: "Telegram FZ-LLC",
    imgSrc: `${IMG_DIR}/products/Telegram.png`,
    points: POINTS.soso,
  },
  "Tile Trackers": {
    name: "Tile Trackers",
    company: "Tile",
    imgSrc: `${IMG_DIR}/products/Tile_Trackers.png`,
    points: POINTS.soso,
  },
  "Google Hangouts": {
    name: "Google Hangouts",
    company: "Google",
    imgSrc: `${IMG_DIR}/products/Google_Hangouts.png`,
    points: POINTS.soso,
  },
  "Video Doorbells": {
    name: "Video Doorbells",
    company: "Google Nest",
    imgSrc: `${IMG_DIR}/products/Google_Nest_Video_Doorbell.png`,
    points: POINTS.soso,
  },
  "Facebook Portal": {
    name: "Facebook Portal",
    company: "Facebook",
    imgSrc: `${IMG_DIR}/products/Facebook_Portal.png`,
    points: POINTS.bad,
  },
  "Echo Studio": {
    name: "Echo Studio",
    company: "Amazon",
    imgSrc: `${IMG_DIR}/products/Amazon_Echo_Studio.png`,
    points: POINTS.bad,
  },
  "Ring Security Cam": {
    name: "Ring Security Cam",
    company: "Amazon",
    imgSrc: `${IMG_DIR}/products/Amazon_Ring_Security_Camera.png`,
    points: POINTS.bad,
  },
  WeChat: {
    name: "WeChat",
    company: "Tencent",
    imgSrc: `${IMG_DIR}/products/WeChat.png`,
    points: POINTS.bad,
  },
  "Streaming Sticks": {
    name: "Streaming Sticks",
    company: "Roku",
    imgSrc: `${IMG_DIR}/products/Roku_Streaming_Sticks.png`,
    points: POINTS.bad,
  },
  Nook: {
    name: "Nook",
    company: "Barnes and Noble",
    imgSrc: `${IMG_DIR}/products/Barnes_Noble_Nook.png`,
    points: POINTS.bad,
  },
};

export const RESULTS = {
  "open book": {
    minPoints: 9,
    heading: "You’re an open book.",
    description:
      "The products and apps you use collect a lot of your personal information. Data brokers send their thanks! But don’t worry — you’re not alone. Even the privacy researchers at Mozilla use some of the same products and apps. If you’re uncomfortable with your quiz results, try opting out of data sharing whenever possible. And choose alternative tech that is more privacy conscious:",
    imgSrc: `${IMG_DIR}/emoji-open-book.png`,
  },
  soso: {
    minPoints: 5,
    heading: "Your privacy is so-so.",
    description:
      "Your online privacy could be worse — but it could be better, too. While some of the products and apps you use value privacy, others are collecting and sharing a good amount of personal data. If you’re okay with that balance, no problem. If you’d like a little more privacy, find alternatives:",
    imgSrc: `${IMG_DIR}/emoji-soso.png`,
  },
  "off the grid": {
    minPoints: 0,
    heading: "You’re off the grid.",
    description:
      "Woah — you take your online privacy and security seriously. That’s no easy feat these days, when everything from connected litterboxes to smart water bottles are after your data. When you get a break from scouring privacy policies and encrypting all the things, why not share some privacy tips with your friends and family?",
    imgSrc: `${IMG_DIR}/emoji-off-the-grid.png`,
  },
};
