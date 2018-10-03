import React from 'react';

/**
 * In order to move fast and not break things, we're doing petition localisation
 * very specifically in a way that only works for petitions, and not for localization
 * in general. The following "looks like JSON" structure is not a .json file because
 * it's actually JSX source code, because of the privacy policy string, which includes
 * a link element.
 */
export default {

  // English
  "en": {
    "First name": `First name`,
    "Please enter your given name(s)": `Please enter your given name(s)`,
    "Last name": `Last name`,
    "Please enter your surname": `Please enter your surname`,
    "Email address": `Email address`,
    "Please enter your email": `Please enter your email`,
    "Your country": `Your country`,
    "Please enter your country": `Please enter your country`,
    "Postal code": `Postal code`,
    "Please enter your postal code": `Please enter your postal code`,
    "Comment": `Comment`,
    "Please include a comment": `Please include a comment`,
    "Something went wrong. Please check your email address and try again": `Something went wrong. Please check your email address and try again`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice": <span>I'm okay with Mozilla handling my info as explained in this <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a></span>,
    "Please check this box if you want to proceed": `Please check this box if you want to proceed`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Yes, I want to receive email updates about Mozilla’s campaigns.`,
    "Add my name": `Add my name`
  },

  // German
  "de": {
    "First name": `Vorname`,
    "Please enter your given name(s)": `Bitte geben Sie Ihre(n) Vornamen ein`,
    "Last name": `Nachname`,
    "Please enter your surname": `Bitte geben Sie Ihren Nachnamen ein`,
    "Email address": `E-Mail-Adresse`,
    "Please enter your email": `Bitte geben Sie Ihre E-Mail-Adresse ein`,
    "Your country": `Ihr Land`,
    "Please enter your country": `Bitte geben Sie Ihr Land ein`,
    "Postal code": `Postleitzahl`,
    "Please enter your postal code": `Bitte geben Sie Ihre Postleitzahl ein`,
    "Comment": `Kommentar`,
    "Please include a comment": `Bitte geben Sie einen Kommentar ein`,
    "Something went wrong. Please check your email address and try again": `Etwas ist schiefgegangen. Bitte überprüfen Sie Ihre E-Mail-Adresse und versuchen Sie es erneut`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice": <span>Ich bin einverstanden mit dem Umgang Mozillas mit meinen Informationen wie im <a href="https://www.mozilla.org/privacy/websites/">Datenschutzhinweis</a> beschrieben</span>,
    "Please check this box if you want to proceed": `Aktivieren Sie bitte dieses Kontrollkästchen, um fortzufahren`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Ja, ich möchte per E-Mail Neuigkeiten über Mozillas Kampagnen erfahren.`,
    "Add my name": `Meinen Namen hinzufügen`
  },

  // French
  "fr": {
    "First name": `Prénom`,
    "Please enter your given name(s)": `Veuillez saisir votre prénom`,
    "Last name": `Nom`,
    "Please enter your surname": `Veuillez saisir votre nom de famille`,
    "Email address": `Adresse électronique`,
    "Please enter your email": `Veuillez saisir votre adresse électronique`,
    "Your country": `Votre pays`,
    "Please enter your country": `Veuillez sélectionner votre pays`,
    "Postal code": `Code postal`,
    "Please enter your postal code": `Veuillez saisir votre code postal`,
    "Comment": `Commentaire`,
    "Please include a comment": `Veuillez ajouter un commentaire`,
    "Something went wrong. Please check your email address and try again": `Une erreur s’est produite. Veuillez vérifier votre adresse électronique et réessayer`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice": <span>J’accepte que Mozilla utilise mes informations conformément à <a href="https://www.mozilla.org/privacy/websites/">cette politique de confidentialité</a></span>,
    "Please check this box if you want to proceed": `Veuillez cocher cette case si vous désirez poursuivre`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `J’accepte de recevoir des informations par courriel au sujet des campagnes de Mozilla.`,
    "Add my name": `Ajouter mon nom`
  },

  // Polish
  "pl": {
    "First name": `Imię`,
    "Please enter your given name(s)": `Proszę podać imię (lub imiona)`,
    "Last name": `Nazwisko`,
    "Please enter your surname": `Proszę podać nazwisko`,
    "Email address": `Adres e-mail`,
    "Please enter your email": `Proszę podać adres e-mail`,
    "Your country": `Kraj`,
    "Please enter your country": `Proszę podać kraj`,
    "Postal code": `Kod pocztowy`,
    "Please enter your postal code": `Proszę podać kod pocztowy`,
    "Comment": `Komentarz`,
    "Please include a comment": `Proszę dołączyć komentarz`,
    "Something went wrong. Please check your email address and try again": `Coś się nie powiodło. Proszę sprawdzić poprawność adresu e-mail i spróbować ponownie`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice": <span>Pozwalam Mozilli wykorzystywać te informacje w sposób opisany w <a href="https://www.mozilla.org/privacy/websites/">zasadach ochrony prywatności</a></span>,
    "Please check this box if you want to proceed": `Proszę zaznaczyć to pole, aby kontynuować`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Tak, chcę otrzymywać wiadomości o kampaniach Mozilli.`,
    "Add my name": `Podpisz`
  }

};
