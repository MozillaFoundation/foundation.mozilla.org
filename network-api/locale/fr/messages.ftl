pulse-author = Par {$authorList}

form-checkbox = Veuillez cocher cette case si vous désirez poursuivre.
back-to-menu = Retour au menu
no-thanks-button = Non merci
first-name =
    .placeholder = Prénom
last-name =
    .placeholder = Nom
country =
    .label = Pays
select-country =
    .aria-label = Veuillez sélectionner votre pays
language-dropdown =
    .aria-label = Veuillez sélectionner une langue
thanks = Merci !
email-label = Adresse électronique
email-input =
    .placeholder = Veuillez saisir votre adresse électronique
    .aria-label = Adresse électronique
sign-up-button = Je m’inscris
cta-header = Protégez Internet en tant que bien commun
cta-description = Rejoignez la lettre d’information <strong>Actualité de Mozilla</strong> pour agir et vous tenir au courant !
privacy-policy = J’accepte que Mozilla utilise mes informations conformément à <privacyLink>cette politique de confidentialité</privacyLink>.
thanks = Merci !
cta-double-opt-in = Si vous n’avez pas précédemment confirmé votre abonnement aux courriels liés à Mozilla, vous devrez peut-être le faire maintenant. <strong>Veuillez vérifier votre boîte de réception ou vos courriers indésirables et recherchez un message de notre part pour confirmer votre abonnement</strong>.
cta-manage-subscriptions = Si vous avez déjà confirmé votre abonnement aux courriels liés à Mozilla, vous pouvez maintenant <preferencesLink>gérer vos abonnements</preferencesLink> et modifier vos préférences de messagerie.
form-error = Une erreur s’est produite. Veuillez vérifier votre adresse électronique et réessayer.
form-email-invalid = Veuillez saisir une adresse électronique valide.
form-field-required = Ce champ est nécessaire.

comments-limit = {$limit ->
    [one] Les commentaires ne peuvent pas dépasser {$limit} caractère
    *[other] Les commentaires ne peuvent pas dépasser {$limit} caractères
}

# Share buttons
email-button = Courriel
share-by-email = Partager par courriel
share-twitter = Partager sur Twitter
share-facebook = Partager sur Facebook
copy-button = Copier
    .data-success-text = Copié
tooltip-copied = Copié
tooltip-copy = Copier
tooltip-page-copy = Copier le lien vers la page
tooltip-page-copied = Lien copié
link-copied =
    .title = Copié
link-copy =
    .title = Copier dans le presse-papiers le lien vers la page

# Petition form
add-my-name-header = Ajoutez votre nom
petition-first-name =
    .label = Prénom
petition-first-name-error = Veuillez saisir votre prénom
petition-last-name =
    .label = Nom
petition-last-name-error = Veuillez saisir votre nom de famille
petition-email =
    .label = Adresse électronique
petition-email-error = Veuillez saisir votre adresse électronique
petition-country =
    .label = Votre pays
petition-country-error = Veuillez sélectionner votre pays
petition-postal-code =
    .label = Code postal
petition-postal-code-error = Veuillez saisir votre code postal
petition-comment =
    .label = Commentaire
petition-comment-error = Veuillez ajouter un commentaire
petition-signup = J’accepte de recevoir des informations par courriel au sujet des campagnes de Mozilla.
add-my-name-button = Ajouter mon nom
petition-error = Une erreur s’est produite lors de la signature de la pétition. Veuillez réessayer plus tard.

# Buyer’s Guide
join-us =
    .flowHeading = Vous avez voté ! Bravo !
    .flowText = Pourquoi ne pas en profiter pour rejoindre Mozilla ? Nous nous battons justement contre ces choses flippantes et nous avons besoin de plus de gens comme vous.
voted-header = {$voteCount ->
    [one] {$voteCount} vote — invitez vos amis à voter !
   *[other] {$voteCount} votes — invitez vos amis à voter !
}

# Creep-o-meter vote
tell-us = Dites-nous ce que vous en pensez
how-creepy = À quel point pensez-vous que ce produit est flippant ?
how-likely-buy = Quelle est la probabilité que vous l’achetiez ?
how-likely-use = Quelle est la probabilité que vous l’utilisiez ?
likely = C’est probable
not-likely = C’est peu probable
vote-button = Voter et voir les résultats
vote-counter = {$voteCount ->
    [one] {$voteCount} vote
   *[other] {$voteCount} votes
}
close-button = Fermer
modal-close-button =
    .aria-label = Fermer

slider =
    .aria-label = Veuillez indiquer à quel point vous considérez ce produit flippant sur une échelle de 0 (pas du tout flippant) à 100 (super flippant)
not-creepy = Pas flippant
super-creepy = Super flippant
percent = {$percent} %
percent-likely-to-buy = {$perc} % pourraient l’acheter
percent-likely-to-use = {$perc} % pourraient l’utiliser
percent-not-likely-to-buy = {$perc} % pensent ne pas l’acheter
percent-not-likely-to-use = {$perc} % pensent ne pas l’utiliser

share-text = Je pense que ce produit {$product} est {$creepType}. Qu’en pensez-vous ? Regardez le flippomètre du guide d’achat {$link} de {$twitterHandle}.
email = Courriel
copy = Copier
