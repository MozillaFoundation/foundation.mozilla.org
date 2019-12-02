import React from 'react';
import enMessages from '../../../../network-api/locale/en/messages.js';
import deMessages from '../../../../network-api/locale/de/messages.js';
import esMessages from '../../../../network-api/locale/es/messages.js';
import frMessages from '../../../../network-api/locale/fr/messages.js';
import plMessages from '../../../../network-api/locale/pl/messages.js';
import ptMessages from '../../../../network-api/locale/pt/messages.js';
import { setupI18n } from '@lingui/core'
import { getCurrentLanguage } from "../petition/locales";


let catalogs = {
  en: enMessages,
  de: deMessages,
  es: esMessages,
  fr: frMessages,
  pl: plMessages,
  pt: ptMessages
};

let i18n = setupI18n({
  language: getCurrentLanguage(),
  catalogs: catalogs,
});


export { catalogs, i18n };
