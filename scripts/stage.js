let NodeGit = require(`nodegit`);
let shell = require(`shelljs`);
let pathToRepo = require(`path`).resolve(`.`);

let getStatus = (repo) => repo.getStatus();

let runDeploy = (remote) => {
  shell.echo(`Running deployment now...`);

  shell.exec(`npm run build`);

  shell.echo(`${new Date}\n\n\n`).to(`last-built.txt`);
  shell.exec(`git log -n 1 >> last-built.txt`);

  shell.exec(`git branch -D gh-pages`);
  shell.exec(`git checkout --orphan gh-pages`);

  shell.rm(`.gitignore`);

  shell.echo(`/*\n`).toEnd(`.gitignore`);
  shell.echo(`!css\n`).toEnd(`.gitignore`);
  shell.echo(`!images\n`).toEnd(`.gitignore`);
  shell.echo(`!index.html\n`).toEnd(`.gitignore`);
  shell.echo(`!last-built.txt\n`).toEnd(`.gitignore`);

  shell.mv(`dest/*`, `./`);

  shell.exec(`git reset`);
  shell.exec(`git add .`);
  shell.exec(`git commit -m 'Deployed via stage.js script'`);
  shell.exec(`git push ${remote} gh-pages -f`);

  shell.echo(`Finished deploying!`);
};

// Check that local repo is clean before deploying

NodeGit.Repository.open(pathToRepo)
  .then(getStatus)
  .then(status => {
    if (status.length) {
      shell.echo(`Repo is dirty. Aborting deploy!`);
      shell.exit(1);
    } else {
      // Check for remote argument
      if (process.argv[2]) {
        runDeploy(process.argv[2]);
      } else {
        shell.echo(`Missing target remote!`);
        shell.exit(2);
      }
    }
  });
