// Before we do ANYTHING else, verify that there are drivers in the main dir.
// If there aren't, then this is going to crash and burn, and whoever's trying
// to run this should "install" the firefox and chrome drivers for their OS.

const fs = require('fs');

const geckoDriver = fs.existsSync('./geckoDriver') || fs.existsSync('./geckoDriver.exe');
if (!geckoDriver) {
  console.log("Missing geckoDriver, please visit https://github.com/mozilla/geckodriver/releases and download the driver for your platform.");
}

const chromeDriver = fs.existsSync('./chromeDriver') || fs.existsSync('./chromeDriver.exe');

if (!chromeDriver) {
  console.log("Missing chromeDriver, please visit http://chromedriver.chromium.org/ and download the driver for your chrome/platform combination.");
}

if (!geckoDriver || !chromeDriver) {
  console.log("\nCannot perform selenium-based site testing due to missing webdrivers.\n");
  process.exit(1);
}


// With that part taken care of, on to the site testing:
require('dotenv').config();
const {Builder, By, Key, until} = require('selenium-webdriver');
const { assert } = require('chai');
const drivers = { firefox: false, chrome: false };

async function buildFF() {
  const firefox = require('selenium-webdriver/firefox');
  const firefoxOptions = new firefox.Options().setBinary(process.env.FIREFOX_BINARY).headless();
  const firefoxDriver = await new Builder().forBrowser('firefox').setFirefoxOptions(firefoxOptions).build();
  drivers.firefox = firefoxDriver;
  return firefoxDriver
}

async function getFF() {
  if (drivers.firefox) return drivers.firefox;
  return buildFF();
}

async function buildChrome() {
  const chrome = require('selenium-webdriver/chrome');
  const chromeOptions = new chrome.Options().setChromeBinaryPath(process.env.CHROME_BINARY).headless().addArguments(`--no-sandbox`);
  const chromeDriver = await new Builder().forBrowser('chrome').setChromeOptions(chromeOptions).build();
  drivers.chrome = chromeDriver;
  return chromeDriver;
}

async function getChrome() {
  if (drivers.chromeDriver) return drivers.chromeDriver;
  return buildChrome();
}

describe('DefaultTest', () => {
  driver = false;

  before(async () => (driver = await getFF()));

  it('Should load the homepage', async() => {
    await driver.get('http://localhost:8000');
  });

  it('Should find the "About Us" nav item', async() => {
    let about = await driver.findElement(By.linkText('About Us'));
    await about.click();
    await driver.wait(until.titleIs('Mozilla Foundation - About Us'), 1000);
  });

  it ('Should see seven secondary menu items on the About Us page', async() => {
    const menuCount = 7;
    let secondary = await driver.findElements(By.css('#multipage-nav .multipage-link'));
    assert.lengthOf(secondary, menuCount, `There should be ${menuCount} secondary nav items`);
  });

  it('Should see the "overview" secondary nav item as active by default', async() => {
    let initial = await driver.findElement(By.linkText('Overview'));
    let classes = await initial.getAttribute('class');
    assert.include(classes.split(/\s+/), 'active', "First menu items is higlighted by default");
  });
});
