// This is essentially middleware between the Pulse API and the Network.
// Eventually this should be replaced by new or modified routes on Pulse that return only the data we need.
// More info -> https://github.com/mozilla/network/issues/372

let unfiltered = {
  pulseInnovation: require(`../source/json/temp/pulse-innovation.json`).results,
  pulseInclusion: require(`../source/json/temp/pulse-inclusion.json`).results,
  pulseDecentralization: require(`../source/json/temp/pulse-decentralization.json`).results,
  pulsePrivacy: require(`../source/json/temp/pulse-privacy.json`).results,
  pulseLiteracy: require(`../source/json/temp/pulse-literacy.json`).results
};

let maxProjectsPerCategory = 2;

let massaged = {
  pulseInnovation: unfiltered.pulseInnovation.slice(0, maxProjectsPerCategory),
  pulseInclusion: undefined,
  pulseDecentralization: undefined,
  pulsePrivacy: undefined,
  pulseLiteracy: undefined
};

// Get pool of all projects currently used
let getPool = (currentCategory) => {
  let pool = [];

  Object.keys(massaged).forEach((key) => {
    if (key !== currentCategory && massaged[key]) {
      pool = pool.concat(massaged[key]);
    }
  });

  return pool;
};

Object.keys(massaged).forEach((key) => {
  let pool = getPool(key);
  let unfilteredProjects = unfiltered[key];
  let filtered = [];

  // Remove any duplicates from current project list
  unfilteredProjects.forEach((project) => {
    let isDuplicate = false;

    pool.forEach((item) => {
      if (project.id === item.id) {
        isDuplicate = true;
      }
    });

    if (!isDuplicate) {
      filtered.push(project);
    }
  });

  // Trim projects list to maximum length
  filtered = filtered.slice(0, maxProjectsPerCategory);

  massaged[key] = filtered;
});


module.exports = massaged;
