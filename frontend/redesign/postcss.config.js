import autoprefixer from "autoprefixer";

const isDev = process.env.NODE_ENV !== 'production';

export default {
  plugins: [autoprefixer],
  map: isDev ? {
    inline: false,
    annotation: true,
    sourcesContent: true
  } : false
};
