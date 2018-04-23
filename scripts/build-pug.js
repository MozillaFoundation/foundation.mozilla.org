let propertiesToObject = require(`java.properties.js`).default;
let pug = require(`pug`);
let shelljs = require(`shelljs`);
let moment = require(`moment`);

let rawStrings = shelljs.cat(`locales/en-US/general.properties`);

function buildPage(template, target, extraData, isDjangoTemplate = false) {
  let viewData = {
    strings: propertiesToObject(rawStrings.toString()),
    templateID: isDjangoTemplate ? `{% block bodyID %}{% endblock %}` : template,
    target: isDjangoTemplate ? `{{ page.get_absolute_url }}` : target,
    data: extraData,
    moment: moment
  };

  let fn = pug.compileFile(`source/pug/${ isDjangoTemplate ? `templates` : `views` }/${template}.pug`, {
    pretty: true
  });

  let html = fn(viewData);

  if (!isDjangoTemplate) {
    let path = `network-api/networkapi/frontend${target}`;

    shelljs.mkdir(`-p`, path);
    shelljs.ShellString(html).to(`${path}/index.html`);
  } else {
    shelljs.ShellString(html).to(target);
  }
}

// Base Template For Mezzanine And Wagtail
buildPage(`base-for-django`, `network-api/networkapi/templates/pages/base-compiled.html`, null, true);
