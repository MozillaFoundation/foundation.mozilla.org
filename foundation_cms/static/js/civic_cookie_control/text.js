// Localized text for Cookie Control v9 (Civic UK)
// English is the default; other locales only need keys that differ.
// CookieControl text keys: https://cookiecontrol.com/docs/v9/

const LOCALE_TEXT = {
  en: {
    text: {
      // notify banner
      notifyTitle: "Help Mozilla with Analytics",
      notifyDescription:
        "We use some essential cookies to make this website. We'd like to set additional cookies to understand how you use mozillafoundation.org. Your settings improve our services.",
      accept: "Accept Analytics Cookies",
      reject: "Reject Analytics Cookies",
      settings: "Consent Settings",
      // setting panel
      title: "Privacy Preference Center",
      intro:
        "When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. This information might be about you, your preferences or your device and is mostly used to make the site work as you expect it to. The information does not usually directly identify you, but it can give you a more personalized web experience. Because we respect your right to privacy, you can choose not to allow some types of cookies. Click on the different category headings to find out more and change our default settings. However, blocking some types of cookies may impact your experience of the site and the services we are able to offer.",
      acceptSettings: "Allow All",
      rejectSettings: "Reject All",
      necessaryTitle: "Necessary Cookies",
      necessaryDescription:
        "These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.",
      // visible label / aria-label for the close button
      closeLabel: "Closeee",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "Functional Cookies",
        description:
          "These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly.",
      },
      {
        name: "performance",
        label: "Performance Cookies",
        description:
          "These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance.",
      },
      {
        name: "personalized_advertising",
        label: "Personalized Advertising Cookies",
        description:
          "These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising.",
      },
    ],
  },
  // Civic doesn't accept hyphenated codes; fy-NL and pt-BR are shortened to "fy" and "pt"
  // Catalan
  ca: {
    text: {
      // notify banner
      notifyTitle: "[WIP]",
      notifyDescription: "[WIP]",
      accept: "[WIP]",
      reject: "[WIP]",
      settings: "[WIP]",
      // setting panel
      title: "[WIP] Títol (CA)",
      intro: "[WIP]",
      acceptSettings: "[WIP]",
      rejectSettings: "[WIP]",
      necessaryTitle: "[WIP]",
      necessaryDescription: "[WIP]",
      // visible label / aria-label for the close button
      closeLabel: "[WIP]",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // German
  de: {
    text: {
      // notify banner
      notifyTitle: "Helfen Sie Mozilla mit Analytics",
      notifyDescription:
        "Wir verwenden notwendige Cookies, um diese Website funktionsfähig zu gestalten. Wir möchten zusätzlich Cookies setzen, um zu verstehen, wie Sie mozillafoundation.org nutzen. Ihre Einstellungen verbessern unsere Dienste.",
      accept: "Alle Cookies akzeptieren",
      reject: "Alle ablehnen",
      settings: "Cookie-Einstellungen",
      // setting panel
      title: "Datenschutz-Präferenz-Center",
      intro:
        "Wenn Sie eine Website besuchen, kann diese Informationen über Ihren Browser abrufen oder speichern. Dies geschieht meist in Form von Cookies. Hierbei kann es sich um Informationen über Sie, Ihre Einstellungen oder Ihr Gerät handeln. Meist werden die Informationen verwendet, um die erwartungsgemäße Funktion der Website zu gewährleisten. Durch diese Informationen werden Sie normalerweise nicht direkt identifiziert. Dadurch kann Ihnen aber ein personalisierteres Web-Erlebnis geboten werden. Da wir Ihr Recht auf Datenschutz respektieren, können Sie sich entscheiden, bestimmte Arten von Cookies nicht zulassen. Klicken Sie auf die verschiedenen Kategorieüberschriften, um mehr zu erfahren und unsere Standardeinstellungen zu ändern. Die Blockierung bestimmter Arten von Cookies kann jedoch zu einer beeinträchtigten Erfahrung mit der von uns zur Verfügung gestellten Website und Dienste führen.",
      acceptSettings: "Alle zulassen",
      rejectSettings: "Alle ablehnen",
      necessaryTitle: "Unbedingt erforderliche Cookies",
      necessaryDescription:
        "Diese Cookies sind zur Funktion der Website erforderlich und können in Ihren Systemen nicht deaktiviert werden. In der Regel werden diese Cookies nur als Reaktion auf von Ihnen getätigte Aktionen gesetzt, die einer Dienstanforderung entsprechen, wie etwa dem Festlegen Ihrer Datenschutzeinstellungen, dem Anmelden oder dem Ausfüllen von Formularen. Sie können Ihren Browser so einstellen, dass diese Cookies blockiert oder Sie über diese Cookies benachrichtigt werden. Einige Bereiche der Website funktionieren dann aber nicht. Diese Cookies speichern keine personenbezogenen Daten.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // Spanish
  es: {
    text: {
      // notify banner
      notifyTitle: "Ayuda a Mozilla con Analytics",
      notifyDescription:
        "Usamos algunas cookies esenciales para hacer este sitio web. Nos gustaría establecer cookies adicionales para entender cómo usas la página mozillafoundation.org. Tus ajustes mejoran nuestros servicios.",
      accept: "Aceptar todas las cookies",
      reject: "Rechazarlas todas",
      settings: "Configuración de cookies",
      // setting panel
      title: "Centro de preferencia de la privacidad",
      intro:
        "Cuando visita cualquier sitio web, el mismo podría obtener o guardar información en su navegador, generalmente mediante el uso de cookies. Esta información puede ser acerca de usted, sus preferencias o su dispositivo, y se usa principalmente para que el sitio funcione según lo esperado. Por lo general, la información no lo identifica directamente, pero puede proporcionarle una experiencia web más personalizada. Ya que respetamos su derecho a la privacidad, usted puede escoger no permitirnos usar ciertas cookies. Haga clic en los encabezados de cada categoría para saber más y cambiar nuestras configuraciones predeterminadas. Sin embargo, el bloqueo de algunos tipos de cookies puede afectar su experiencia en el sitio y los servicios que podemos ofrecer.",
      acceptSettings: "Permitirlas todas",
      rejectSettings: "Rechazarlas todas",
      necessaryTitle: "Cookies estrictamente necesarias",
      necessaryDescription:
        "Estas cookies son necesarias para que el sitio web funcione y no se pueden desactivar en nuestros sistemas. Usualmente están configuradas para responder a acciones hechas por usted para recibir servicios, tales como ajustar sus preferencias de privacidad, iniciar sesión en el sitio, o llenar formularios. Usted puede configurar su navegador para bloquear o alertar la presencia de estas cookies, pero algunas partes del sitio web no funcionarán. Estas cookies no guardan ninguna información personal identificable.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // French
  fr: {
    text: {
      // notify banner
      notifyTitle: "Aidez Mozilla avec les outils d'analyse",
      notifyDescription:
        "Ce site utilise des cookies essentiels à son fonctionnement. Nous aimerions configurer des cookies supplémentaires pour mieux comprendre comment vous naviguez sur mozillafoundation.org. Vos préférences nous aident à améliorer nos services.",
      accept: "Autoriser tous les cookies",
      reject: "Tout refuser",
      settings: "Paramètres des cookies",
      // setting panel
      title: "Centre de préférences de la confidentialité",
      intro:
        "Lorsque vous consultez un site Web, des données peuvent être stockées dans votre navigateur ou récupérées à partir de celui-ci, généralement sous la forme de cookies. Ces informations peuvent porter sur vous, sur vos préférences ou sur votre appareil et sont principalement utilisées pour s'assurer que le site Web fonctionne correctement. Les informations ne permettent généralement pas de vous identifier directement, mais peuvent vous permettre de bénéficier d'une expérience Web personnalisée. Parce que nous respectons votre droit à la vie privée, nous vous donnons la possibilité de ne pas autoriser certains types de cookies. Cliquez sur les différentes catégories pour obtenir plus de détails sur chacune d'entre elles, et modifier les paramètres par défaut. Toutefois, si vous bloquez certains types de cookies, votre expérience de navigation et les services que nous sommes en mesure de vous offrir peuvent être impactés.",
      acceptSettings: "Tout autoriser",
      rejectSettings: "Tout refuser",
      necessaryTitle: "Cookies strictement nécessaires",
      necessaryDescription:
        "Ces cookies sont nécessaires au fonctionnement du site Web et ne peuvent pas être désactivés dans nos systèmes. Ils sont généralement établis en tant que réponse à des actions que vous avez effectuées et qui constituent une demande de services, telles que la définition de vos préférences en matière de confidentialité, la connexion ou le remplissage de formulaires. Vous pouvez configurer votre navigateur afin de bloquer ou être informé de l'existence de ces cookies, mais certaines parties du site Web peuvent être affectées. Ces cookies ne stockent aucune information d'identification personnelle.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // Frisian
  fy: {
    text: {
      // notify banner
      notifyTitle: "[WIP]",
      notifyDescription: "[WIP]",
      accept: "[WIP]",
      reject: "[WIP]",
      settings: "[WIP]",
      // setting panel
      title: "[WIP] Titel (FY)",
      intro: "[WIP]",
      acceptSettings: "[WIP]",
      rejectSettings: "[WIP]",
      necessaryTitle: "[WIP]",
      necessaryDescription: "[WIP]",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // Dutch
  nl: {
    text: {
      // notify banner
      notifyTitle: "[WIP]",
      notifyDescription: "[WIP]",
      accept: "[WIP]",
      reject: "[WIP]",
      settings: "[WIP]",
      // setting panel
      title: "[WIP] Titel (NL)",
      intro: "[WIP]",
      acceptSettings: "[WIP]",
      rejectSettings: "[WIP]",
      necessaryTitle: "[WIP]",
      necessaryDescription: "[WIP]",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // Polish
  pl: {
    text: {
      // notify banner
      notifyTitle: "[WIP]",
      notifyDescription: "[WIP]",
      accept: "[WIP]",
      reject: "[WIP]",
      settings: "[WIP]",
      // setting panel
      title: "[WIP] Tytuł (PL)",
      intro: "[WIP]",
      acceptSettings: "[WIP]",
      rejectSettings: "[WIP]",
      necessaryTitle: "[WIP]",
      necessaryDescription: "[WIP]",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // Portuguese (Brazil) (pt-BR)
  pt: {
    text: {
      // notify banner
      notifyTitle: "[WIP]",
      notifyDescription: "[WIP]",
      accept: "[WIP]",
      reject: "[WIP]",
      settings: "[WIP]",
      // setting panel
      title: "[WIP] Título (PT)",
      intro: "[WIP]",
      acceptSettings: "[WIP]",
      rejectSettings: "[WIP]",
      necessaryTitle: "[WIP]",
      necessaryDescription: "[WIP]",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
  // Swahili
  sw: {
    text: {
      // notify banner
      notifyTitle: "[WIP]",
      notifyDescription: "[WIP]",
      accept: "[WIP]",
      reject: "[WIP]",
      settings: "[WIP]",
      // setting panel
      title: "[WIP] Kichwa (SW)",
      intro: "[WIP]",
      acceptSettings: "[WIP]",
      rejectSettings: "[WIP]",
      necessaryTitle: "[WIP]",
      necessaryDescription: "[WIP]",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    optionalCookies: [
      {
        name: "functional",
        label: "[WIP] Functional Cookies",
        description: "[WIP]",
      },
      {
        name: "performance",
        label: "[WIP] Performance Cookies",
        description: "[WIP]",
      },
      {
        name: "personalized_advertising",
        label: "[WIP] Personalized Advertising Cookies",
        description: "[WIP]",
      },
    ],
  },
};

export default LOCALE_TEXT;
