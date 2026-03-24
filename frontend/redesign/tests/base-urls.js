const REDESIGN_DOMAIN = "http://localhost:8000";

export function foundationBaseUrl(locale = "en") {
  return `${REDESIGN_DOMAIN}/${locale}`;
}
