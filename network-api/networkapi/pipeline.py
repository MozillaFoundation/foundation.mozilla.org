# @TODO Migrate users to auth0's default FirstnameLastname usernames and get rid of this?


def force_username_from_nickname(backend, details, response, *args, **kwargs):
    """
    Forces username to match Google-style nickname for consistency across backends.
    Required to not duplicate users when switched from google-oauth2 to auth0 mozilla sso.
    """
    print("Custom pipeline step running")
    nickname = response.get("nickname") or response.get("given_name") or response.get("name")
    if nickname:
        print("Nickname found")
        details["username"] = nickname.lower().replace(" ", "")
    else:
        print("Nickname not found")