// When adding new sections of the site (e.g. blog, campaigns),
// also add the corresponding backend paths to the workflow trigger and check-changes job in:
// .github/workflows/visual-regression-testing-redesign.yml

const RedesignURLs = {
  Homepage: "/",
  "Nothing Personal Home": "/nothing-personal/",
  "Nothing Personal Article": "/nothing-personal/expert-profile-article-1/",
};

export default RedesignURLs;
