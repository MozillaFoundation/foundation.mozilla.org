// Localized text for Cookie Control v9 (Civic UK)
// English is the default; other locales only need keys that differ.
// CookieControl text keys: https://cookiecontrol.com/docs/v9/
//
// optionalCookies labels/descriptions per locale are defined in TP1-4033.
// TODO(TP1-4033): revise accept/reject button labels across all locales once optional category names are confirmed. "Analytics Cookies" may not be accurate.

const CCPA_CONFIG_SHARED = {
  url: "https://www.civicuk.com/",
  updated: "25/05/2018",
};

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
      closeLabel: "Close",
    },
    ccpaConfig: {
      description:
        "[CCPA Config Description] When you visit our website, we store cookies on your browser to collect information. The information collected might relate to you, your preferences or your device, and is mostly used to make the site work as you expect it to and to provide a more personalized web experience. However, you can choose not to allow certain types of cookies, which may impact your experience of the site and the services we are able to offer. Click on the different category headings to find out more and change our default settings according to your preference. You cannot opt-out of our First Party Strictly Necessary Cookies as they are deployed in order to ensure the proper functioning of our website (such as prompting the cookie banner and remembering your settings, to log into your account, to redirect you when you log out, etc.). For more information about the First and Third Party Cookies used please follow this link.",
      name: "More information",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "Do Not Sell or Share My Personal Information",
    },
  },
  // Civic doesn't accept hyphenated codes; fy-NL and pt-BR are shortened to "fy" and "pt"
  // Catalan
  // Note: OneTrust's Catalan (ca) text appears to be incorrectly mapped to Swahili (sw).
  // Catalan text needs to be sourced separately.
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
    ccpaConfig: {
      description: "[WIP] CCPA intro for Catalan",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
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
    ccpaConfig: {
      description: "[WIP] CCPA intro for German",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
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
    ccpaConfig: {
      description: "[WIP] CCPA intro for Spanish",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
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
    ccpaConfig: {
      description: "[WIP] CCPA intro for French",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
  },
  // Frisian
  // Note: OneTrust's Frisian (fy) text appears to be incorrectly mapped to Swahili (sw).
  // Frisian text needs to be sourced separately.
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
    ccpaConfig: {
      description: "[WIP] CCPA intro for Frisian",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
  },
  // Dutch
  nl: {
    text: {
      // notify banner
      notifyTitle: "Help Mozilla met analyses",
      notifyDescription:
        "We gebruiken een aantal essentiële cookies om deze website te maken. We willen graag extra cookies plaatsen om te begrijpen hoe u mozillafoundation.org gebruikt. Dankzij uw instellingen kunnen we onze dienstverlening verbeteren.",
      accept: "Alle cookies accepteren",
      reject: "Alles afwijzen",
      settings: "Cookie-instellingen",
      // setting panel
      title: "Voorkeurenmenu",
      intro:
        "Wanneer u een website bezoekt, kan er informatie in uw browser worden opgeslagen of eruit worden opgehaald, voornamelijk in de vorm van cookies. Deze informatie kan over u, uw voorkeuren of uw apparaat zijn en wordt voornamelijk gebruikt om de website correct te laten werken. De informatie identificeert u normaal gesproken niet direct, maar kan u een beter op uw voorkeuren toegesneden surfervaring geven. Omdat we uw recht op privacy respecteren, kunt u er voor kiezen sommige soorten cookies te blokkeren. Klik op de namen voor de verschillende categorieën voor meer informatie en om onze standaardinstellingen te wijzigen. Weest u zich er echter wel van bewust dat het blokkeren van sommige soorten cookies uw ervaring van de website en de door ons aangeboden diensten nadelig kan beïnvloeden.",
      acceptSettings: "Alle toestaan",
      rejectSettings: "Alles afwijzen",
      necessaryTitle: "Strikt noodzakelijke cookies",
      necessaryDescription:
        "Deze cookies zijn nodig anders werkt de website niet. Deze cookies kunnen niet worden uitgeschakeld. In de meeste gevallen worden deze cookies alleen gebruikt naar aanleiding van een handeling van u waarmee u in wezen een dienst aanvraagt, bijvoorbeeld uw privacyinstellingen registreren, in de website inloggen of een formulier invullen. U kunt uw browser instellen om deze cookies te blokkeren of om u voor deze cookies te waarschuwen, maar sommige delen van de website zullen dan niet werken. Deze cookies slaan geen persoonlijk identificeerbare informatie op.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    ccpaConfig: {
      description: "[WIP] CCPA intro for Dutch",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
  },
  // Polish
  pl: {
    text: {
      // notify banner
      notifyTitle: "Pomóż nam z analityką",
      notifyDescription:
        "Do stworzenia tej witryny internetowej używamy niezbędnych plików cookie. Chcielibyśmy ustawić dodatkowe pliki cookie, które pomogą nam zrozumieć, w jaki sposób korzystasz z mozillafoundation.org. Twoje ustawienia poprawiają jakość naszych usług.",
      accept: "Akceptuj wszystkie pliki cookie",
      reject: "Odrzucenie wszystkich",
      settings: "Ustawienia plików cookie",
      // setting panel
      title: "Centrum preferencji prywatności",
      intro:
        "Podczas odwiedzania jakiejkolwiek strony internetowej, może ona przechowywać lub pobierać informacje z przeglądarki, głównie w formie plików cookie. Informacje te mogą dotyczyć użytkownika, jego preferencji lub urządzenia i są najczęściej wykorzystywane w celu zapewnienia, że witryna będzie działać tak, jak tego oczekują użytkownicy. Informacje zazwyczaj nie identyfikują bezpośrednio użytkownika, ale mogą zapewnić mu bardziej spersonalizowane doświadczenie w sieci. Ponieważ szanujemy prawo użytkownika do prywatności, użytkownik może zrezygnować z akceptowania niektórych rodzajów plików cookie. Aby dowiedzieć się więcej i zmienić nasze ustawienia domyślne, należy kliknąć na poszczególne nagłówki kategorii. Jednakże blokowanie niektórych rodzajów plików cookie może mieć wpływ na doświadczenia użytkownika związane z witryną i usługami, które możemy zaoferować.",
      acceptSettings: "Zezwolenie na wszystkie",
      rejectSettings: "Odrzucenie wszystkich",
      necessaryTitle: "Ściśle niezbędne pliki cookie",
      necessaryDescription:
        "Te pliki cookie są niezbędne dla funkcjonowania strony internetowej i nie mogą być wyłączone w naszych systemach. Są one zazwyczaj ustawiane tylko w odpowiedzi na działania podejmowane przez użytkownika, które sprowadzają się do zapytania o usługi, takie jak ustawienie preferencji prywatności, logowanie lub wypełnianie formularzy. Można ustawić przeglądarkę tak, aby blokowała lub ostrzegała o tych plikach cookie, ale niektóre części witryny nie będą wtedy działały. Te pliki cookie nie przechowują żadnych danych osobowych.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    ccpaConfig: {
      description: "[WIP] CCPA intro for Polish",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
  },
  // Portuguese
  pt: {
    text: {
      // notify banner
      notifyTitle: "Ajude a Mozilla com o Analytics",
      notifyDescription:
        "Usamos alguns cookies essenciais para criar este site. Gostaríamos de definir cookies adicionais para entender como você usa o mozillafoundation.org. Suas configurações melhoram nossos serviços.",
      accept: "Aceitar todos os cookies",
      reject: "Rejeitar Todos",
      settings: "Definições de cookies",
      // setting panel
      title: "Centro de preferências de privacidade",
      intro:
        "Quando visita um website, este pode armazenar ou recolher informações no seu navegador, principalmente na forma de cookies. Esta informação pode ser sobre si, as suas preferências ou o seu dispositivo e é utilizada principalmente para fazer o website funcionar conforme o esperado. A informação normalmente não o identifica diretamente, mas pode dar-lhe uma experiência web mais personalizada. Uma vez que respeitamos o seu direito à privacidade, pode optar por não permitir alguns tipos de cookies. Clique nos cabeçalhos das diferentes categorias para saber mais e alterar as nossas configurações predefinidas. No entanto, o bloqueio de alguns tipos de cookies pode afetar a sua experiência no website e os serviços que podemos oferecer.",
      acceptSettings: "Permitir todos",
      rejectSettings: "Rejeitar todos",
      necessaryTitle: "Cookies estritamente necessários",
      necessaryDescription:
        "Estes cookies são necessários para que o website funcione e não podem ser desligados nos nossos sistemas. Normalmente, eles só são configurados em resposta a ações levadas a cabo por si e que correspondem a uma solicitação de serviços, tais como definir as suas preferências de privacidade, iniciar sessão ou preencher formulários. Pode configurar o seu navegador para bloquear ou alertá-lo(a) sobre esses cookies, mas algumas partes do website não funcionarão. Estes cookies não armazenam qualquer informação pessoal identificável.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    ccpaConfig: {
      description: "[WIP] CCPA intro for Portuguese",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
  },
  // Swahili
  sw: {
    text: {
      // notify banner
      notifyTitle: "Saidia Mozilla na uchanganuzi",
      notifyDescription:
        "Tunatumia vidakuzi muhimu kutengeneza tovuti hii. Tungependa kuweka vidakuzi vya ziada kuelewa jinsi unavyotumia mozillafoundation.org. Mipangilio yako inaboresha huduma zetu.",
      accept: "Kubali Vidakuzi Vyote",
      reject: "Kataa Yote",
      settings: "Mipangilio ya Vidakuzi",
      // setting panel
      title: "Kituo cha Upendeleo wa Faragha",
      intro:
        "Unapotembelea tovuti yoyote, inaweza kuhifadhi au kupata habari kwenye kivinjari chako, hasa kwa njia ya kuki. Habari hii inaweza kuwa juu yako, mapendekezo yako au kifaa chako na hutumiwa zaidi kufanya tovuti ifanye kazi kama unavyotarajia. Habari hiyo kwa kawaida haikutambui moja kwa moja, lakini inaweza kukupa uzoefu zaidi wa wavuti. Kwa sababu tunaheshimu haki yako ya faragha, unaweza kuchagua kutoruhusu aina fulani za biskuti. Bofya kwenye vichwa vya kategoria tofauti ili kujua zaidi na kubadilisha mipangilio yetu chaguo-msingi. Hata hivyo, kuzuia baadhi ya aina ya cookies inaweza kuathiri uzoefu wako wa tovuti na huduma sisi ni uwezo wa kutoa.",
      acceptSettings: "Ruhusu Yote",
      rejectSettings: "Kataa Yote",
      necessaryTitle: "Vidakuzi vya lazima kabisa",
      necessaryDescription:
        "Vidakuzi hivi ni muhimu kwa tovuti kufanya kazi na haziwezi kuzimwa katika mifumo yetu. Kwa kawaida huwekwa tu kulingana na hatua unazofanya ambazo ni sawa na ombi la huduma, kama vile kuweka mapendeleo yako ya faragha, kuingia au kujaza fomu. Unaweza kuweka kivinjari chako kukuzuia au kukuarifu kuhusu vidakuzi hivi, lakini baadhi ya sehemu za tovuti hazitafanya kazi. Vidakuzi hivi havihifadhi maelezo yoyote yanayoweza kumtambulisha mtu binafsi.",
      // visible label / aria-label for the close button
      closeLabel: "[WIP] Close",
    },
    ccpaConfig: {
      description: "[WIP] CCPA intro for Swahili",
      name: "[WIP] link name",
      ...CCPA_CONFIG_SHARED,
      rejectButton: "[WIP] reject button text",
    },
  },
};

export default LOCALE_TEXT;
