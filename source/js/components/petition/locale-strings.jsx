import { Fragment } from "react";

/**
 * In order to move fast and not break things, we're doing petition localisation
 * very specifically in a way that only works for petitions, and not for localization
 * in general. The following "looks like JSON" structure is not a .json file because
 * it's actually JSX source code, because of the privacy policy string, which includes
 * a link element.
 */
export default {
  // English
  en: {
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
    Comment: `Comment`,
    "Please include a comment": `Please include a comment`,
    "Something went wrong. Please check your email address and try again": `Something went wrong. Please check your email address and try again`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice":
      (
        <span>
          I'm okay with Mozilla handling my info as explained in this{" "}
          <a href="https://www.mozilla.org/privacy/websites/">Privacy Notice</a>
        </span>
      ),
    "Please check this box if you want to proceed": `Please check this box if you want to proceed`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Yes, I want to receive email updates about Mozilla’s campaigns.`,
    "Add my name": `Add my name`,
    "Sign up": `Sign up`,
    "Help shape the future of the web for the public good": `Help shape the future of the web for the public good.`,
    "Join our list": `<p>Join our <b>Mozilla News</b> email list to get action alerts & internet tips right to your inbox.</p>`,
    "This is a required section.": `This is a required section.`,
    "Please enter a valid email address.": `Please enter a valid email address.`,
    "Please check this box if you want to proceed.": `Please check this box if you want to proceed.`,
    "Thanks!": `Thanks!`,
    "confirm your email opt-in": (
      <Fragment>
        If you haven’t previously confirmed your opt-in to a Mozilla-related
        email subscription you may have to do so now.{" "}
        <strong>
          Please check your inbox or spam filter for an email from us to click
          and confirm your subscription
        </strong>
        .
      </Fragment>
    ),
    "manage your subscriptions": (
      <Fragment>
        If you have already confirmed your opt-in to receive Mozilla-related
        emails, you can now{" "}
        <a href="https://www.mozilla.org/newsletter/recovery/" target="_blank">
          manage your subscriptions
        </a>{" "}
        and update your email preferences.
      </Fragment>
    ),
  },

  // German
  de: {
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
    Comment: `Kommentar`,
    "Please include a comment": `Bitte geben Sie einen Kommentar ein`,
    "Something went wrong. Please check your email address and try again": `Etwas ist schiefgegangen. Bitte überprüfen Sie Ihre E-Mail-Adresse und versuchen Sie es erneut`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice":
      (
        <span>
          Ich bin einverstanden mit dem Umgang Mozillas mit meinen Informationen
          wie im{" "}
          <a href="https://www.mozilla.org/privacy/websites/">
            Datenschutzhinweis
          </a>{" "}
          beschrieben
        </span>
      ),
    "Please check this box if you want to proceed": `Aktivieren Sie bitte dieses Kontrollkästchen, um fortzufahren`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Ja, ich möchte per E-Mail Neuigkeiten über Mozillas Kampagnen erfahren.`,
    "Add my name": `Meinen Namen hinzufügen`,
    "Sign up": `Abonnieren`,
    "Help shape the future of the web for the public good": `Gestalten Sie mit uns die Zukunft des Webs zum Wohle der Allgemeinheit.`,
    "Join our list": `<p>Tragen Sie sich in unsere E-Mail-Liste <b>Mozilla News</b> ein, um Benachrichtigungen über Aktionen und Tipps zum Internet direkt in Ihren Posteingang zu erhalten.</p>`,
    "This is a required section.": `Dies ist eine Pflichtangabe.`,
    "Please enter a valid email address.": `Bitte geben Sie eine gültige E-Mail-Adresse ein.`,
    "Please check this box if you want to proceed.": `Bitte setzen Sie hier zum Fortfahren einen Haken.`,
    "Thanks!": `Danke!`,
    "confirm your email opt-in": (
      <Fragment>
        Wenn Sie Ihre Anmeldung für ein Mozilla-E-Mail-Abonnement noch nicht
        bestätigt haben, müssen Sie dies möglicherweise jetzt tun.{" "}
        <strong>
          Bitte sehen Sie in Ihrem Posteingang oder Spam-Filter nach einer
          E-Mail von uns und bestätigen Sie Ihr Abonnement per Mausklick.
        </strong>
      </Fragment>
    ),
    "manage your subscriptions": (
      <Fragment>
        Wenn Sie Ihre Anmeldung zum Empfang von Mozilla-bezogenen E-Mails
        bereits bestätigt haben, können Sie jetzt{" "}
        <a href="https://www.mozilla.org/newsletter/recovery/" target="_blank">
          Ihre Abonnements verwalten
        </a>{" "}
        und Ihre E-Mail-Einstellungen aktualisieren.
      </Fragment>
    ),
  },

  // Spanish
  es: {
    "First name": `Nombre`,
    "Please enter your given name(s)": `Introduce tu nombre`,
    "Last name": `Apellido`,
    "Please enter your surname": `Introduce tu apellido`,
    "Email address": `Dirección de correo electrónico`,
    "Please enter your email": `Introduce tu correo electrónico`,
    "Your country": `País`,
    "Please enter your country": `Introduce tu país`,
    "Postal code": `Código postal`,
    "Please enter your postal code": `Introduce tu código postal`,
    Comment: `Comentario`,
    "Please include a comment": `Por favor, escribe un comentario`,
    "Something went wrong. Please check your email address and try again": `Algo fue mal. Comprueba tu dirección de correo y vuelve a intentarlo`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice":
      (
        <span>
          Estoy de acuerdo con la gestión de mi información, tal y como se
          explica en este{" "}
          <a href="https://www.mozilla.org/privacy/websites/">
            Aviso de privacidad
          </a>
        </span>
      ),
    "Please check this box if you want to proceed": `Marca esta casilla si quieres continuar`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Sí, quiero recibir actualizaciones sobre las campañas de Mozilla.`,
    "Add my name": `Añadir mi nombre`,
    "Sign up": `Suscribirme`,
    "Help shape the future of the web for the public good": `Ayuda a dar forma al futuro de la web para el bien público.`,
    "Join our list": `<p>Únete a nuestra lista de correo electrónico de <b>Noticias de Mozilla</b> para recibir alertas de acción y consejos sobre Internet directamente en tu bandeja de entrada.</p>`,
    "This is a required section.": `Esta sección es obligatoria.`,
    "Please enter a valid email address.": `Escribe una dirección válida de correo electrónico.`,
    "Please check this box if you want to proceed.": `Marca esta casilla si quieres continuar.`,
    "Thanks!": `¡Gracias!`,
    "confirm your email opt-in": (
      <Fragment>
        Si no has confirmado previamente tu aceptación a una suscripción de
        correo electrónico relacionada con Mozilla, es posible que debas hacerlo
        ahora.{" "}
        <strong>
          Revisa tu bandeja de entrada o filtro de correo no deseado para
          encontrar un correo electrónico nuestro para que hagas clic y
          confirmes tu suscripción.
        </strong>
        .
      </Fragment>
    ),
    "manage your subscriptions": (
      <Fragment>
        Si ya has confirmado tu aceptación para recibir correos electrónicos
        relacionados con Mozilla, ahora puedes{" "}
        <a href="https://www.mozilla.org/newsletter/recovery/" target="_blank">
          administrar tus suscripciones
        </a>{" "}
        y actualizar tus preferencias de correo electrónico.
      </Fragment>
    ),
  },

  // French
  fr: {
    "First name": `Prénom`,
    "Please enter your given name(s)": `Veuillez saisir votre prénom`,
    "Last name": `Nom`,
    "Please enter your surname": `Veuillez saisir votre nom de famille`,
    "Email address": `Adresse e-mail`,
    "Please enter your email": `Saisissez votre adresse e-mail`,
    "Your country": `Votre pays`,
    "Please enter your country": `Veuillez sélectionner votre pays`,
    "Postal code": `Code postal`,
    "Please enter your postal code": `Veuillez saisir votre code postal`,
    Comment: `Commentaire`,
    "Please include a comment": `Veuillez ajouter un commentaire`,
    "Something went wrong. Please check your email address and try again": `Une erreur s’est produite. Veuillez vérifier votre adresse électronique et réessayer`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice":
      (
        <span>
          J’accepte que Mozilla utilise mes informations conformément à{" "}
          <a href="https://www.mozilla.org/privacy/websites/">
            cette politique de confidentialité
          </a>
        </span>
      ),
    "Please check this box if you want to proceed": `Veuillez cocher cette case si vous désirez poursuivre`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `J’accepte de recevoir des informations par e-mail au sujet des campagnes de Mozilla.`,
    "Add my name": `Ajouter mon nom`,
    "Sign up": `Je m’inscris`,
    "Help shape the future of the web for the public good": `Aidez à façonner l’avenir du Web pour le bien commun.`,
    "Join our list": `<p>Abonnez-vous à notre newsletter <b>Actualités de Mozilla</b> pour recevoir des conseils pour Internet et des alertes pour passer à l’action.</p>`,
    "This is a required section.": `Ce champ est obligatoire.`,
    "Please enter a valid email address.": `Veuillez indiquer une adresse e-mail valide.`,
    "Please check this box if you want to proceed.": `Cochez cette case si vous souhaitez continuer.`,
    "Thanks!": `Merci !`,
    "confirm your email opt-in": (
      <Fragment>
        Si vous n’avez pas précédemment confirmé votre abonnement aux e-mails
        liés à Mozilla, vous devrez peut-être le faire maintenant.{" "}
        <strong>
          Veuillez vérifier votre boîte de réception ou vos courriers
          indésirables et recherchez un message de notre part pour confirmer
          votre abonnement.
        </strong>
      </Fragment>
    ),
    "manage your subscriptions": (
      <Fragment>
        Si vous avez déjà confirmé votre abonnement aux e-mails liés à Mozilla,
        vous pouvez maintenant{" "}
        <a href="https://www.mozilla.org/newsletter/recovery/" target="_blank">
          gérer vos abonnements
        </a>{" "}
        et modifier vos préférences de messagerie.
      </Fragment>
    ),
  },

  // Polish
  pl: {
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
    Comment: `Komentarz`,
    "Please include a comment": `Proszę dołączyć komentarz`,
    "Something went wrong. Please check your email address and try again": `Coś się nie powiodło. Proszę sprawdzić poprawność adresu e-mail i spróbować ponownie`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice":
      (
        <span>
          Pozwalam Mozilli wykorzystywać te informacje w sposób opisany w{" "}
          <a href="https://www.mozilla.org/privacy/websites/">
            zasadach ochrony prywatności
          </a>
        </span>
      ),
    "Please check this box if you want to proceed": `Proszę zaznaczyć to pole, aby kontynuować`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Tak, chcę otrzymywać wiadomości o kampaniach Mozilli.`,
    "Add my name": `Podpisz`,
    "Sign up": `Zapisz się`,
    "Help shape the future of the web for the public good": `Pomóż kształtować przyszłość Internetu dla wspólnego dobra.`,
    "Join our list": `<p>Dołącz do naszej listy <b>Aktualności Mozilli</b>, aby otrzymywać powiadomienia o możliwościach działania i wskazówki o Internecie prosto do swojej skrzynki.</p>`,
    "This is a required section.": `To jest wymagana sekcja.`,
    "Please enter a valid email address.": `Wpisz prawidłowy adres e-mail.`,
    "Please check this box if you want to proceed.": `Zaznacz to pole, aby kontynuować.`,
    "Thanks!": `Dziękujemy!`,
    "confirm your email opt-in": (
      <Fragment>
        Jeśli jeszcze nigdy nie potwierdzono zgody na subskrypcję wiadomości od
        Mozilli, to możesz musieć zrobić to teraz.{" "}
        <strong>
          Sprawdź, czy w skrzynce odbiorczej lub spamie jest wiadomość od nas,
          aby kliknąć i potwierdzić subskrypcję.
        </strong>
      </Fragment>
    ),
    "manage your subscriptions": (
      <Fragment>
        Jeśli już potwierdzono zgodę na otrzymywanie wiadomości od Mozilli, to
        można teraz{" "}
        <a href="https://www.mozilla.org/newsletter/recovery/" target="_blank">
          zarządzać swoimi subskrypcjami
        </a>{" "}
        i zaktualizować preferencje.
      </Fragment>
    ),
  },

  // Portuguese
  "pt-BR": {
    "First name": `Nome`,
    "Please enter your given name(s)": `Insira seu nome`,
    "Last name": `Sobrenome`,
    "Please enter your surname": `Insira seu sobrenome`,
    "Email address": `Endereço de e-mail`,
    "Please enter your email": `Insira seu e-mail`,
    "Your country": `Seu país`,
    "Please enter your country": `Insira seu país`,
    "Postal code": `CEP`,
    "Please enter your postal code": `Insira seu CEP`,
    Comment: `Comentário`,
    "Please include a comment": `Inclua um comentário`,
    "Something went wrong. Please check your email address and try again": `Algo deu errado. Verifique seu endereço de e-mail e tente novamente`,
    "I'm okay with Mozilla handling my info as explained in this Privacy Notice":
      (
        <span>
          Concordo com a Mozilla lidar com minhas informações, como explicado
          neste{" "}
          <a href="https://www.mozilla.org/privacy/websites/">
            Aviso de Privacidade
          </a>
        </span>
      ),
    "Please check this box if you want to proceed": `Marque esta opção se deseja continuar`,
    "Yes, I want to receive email updates about Mozilla's campaigns.": `Quero receber atualizações por e-mail sobre campanhas da Mozilla.`,
    "Add my name": `Adicionar meu nome`,
    "Sign up": `Inscreva-me`,
    "Help shape the future of the web for the public good": `Ajude a moldar o futuro da web para o bem público.`,
    "Join our list": `<p>Junte-se à nossa lista de emails <b>Mozilla News</b> para receber alertas de ações e dicas de internet direto na sua caixa de entrada.</p>`,
    "This is a required section.": `Este campo é obrigatório.`,
    "Please enter a valid email address.": `Insira um endereço de e-mail válido.`,
    "Please check this box if you want to proceed.": `Selecione esta caixa para continuar.`,
    "Thanks!": `Obrigado!`,
    "confirm your email opt-in": (
      <Fragment>
        Se você não confirmou anteriormente sua inscrição em uma assinatura de
        e-mail relacionada à Mozilla, pode ser necessário fazê-lo agora.{" "}
        <strong>
          Verifique se há um e-mail nosso, na caixa de entrada ou no filtro de
          spam, para clicar e confirmar sua assinatura.
        </strong>
      </Fragment>
    ),
    "manage your subscriptions": (
      <Fragment>
        Se você já confirmou sua inscrição para receber e-mails relacionados à
        Mozilla, agora pode{" "}
        <a href="https://www.mozilla.org/newsletter/recovery/" target="_blank">
          gerenciar suas assinaturas
        </a>{" "}
        e atualizar suas preferências de e-mail.
      </Fragment>
    ),
  },
};
