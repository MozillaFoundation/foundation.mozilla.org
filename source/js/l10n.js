import "intl-pluralrules";
import { FluentBundle, FluentResource } from "@fluent/bundle";
import { negotiateLanguages } from "@fluent/langneg";
import { ReactLocalization } from "@fluent/react";
import { getCurrentLanguage } from "./components/petition/locales";

import deMessages from "../../network-api/locale/de/messages.ftl";
import esMessages from "../../network-api/locale/es/messages.ftl";
import frMessages from "../../network-api/locale/fr/messages.ftl";
import plMessages from "../../network-api/locale/pl/messages.ftl";
import ptMessages from "../../network-api/locale/pt_BR/messages.ftl";
import sourceMessages from "../../network-api/locale/messages.ftl";

const LOCALES = ["de", "en", "es", "fr", "pl", "pt"];

const MESSAGES_ALL = {
  de: deMessages,
  en: sourceMessages,
  es: esMessages,
  fr: frMessages,
  pl: plMessages,
  pt: ptMessages,
};

export function getBundles() {
  // Choose locales that are best for the user.
  const currentLocales = negotiateLanguages([getCurrentLanguage()], LOCALES, {
    defaultLocale: "en",
  });

  const bundles = [];

  for (const locale of currentLocales) {
    let resource = new FluentResource(MESSAGES_ALL[locale]);
    const bundle = new FluentBundle(locale);
    bundle.addResource(resource);
    bundles.push(bundle);
  }

  return new ReactLocalization(bundles);
}
