# @TODO Migrate users to auth0's default FirstnameLastname usernames and get rid of this?

def force_username_from_nickname(backend, details, response, *args, **kwargs):
    """
    Forces username to match Google-style nickname for consistency across backends.
    Required to not duplicate users when switched from google-oauth2 to auth0 mozilla sso.
    """
    print("Custom pipeline step running")
    import pprint
    print("Print response")
    pprint.pprint(response)
    print("Print details")
    pprint.pprint(details)

    nickname = (
        response.get("nickname") or
        response.get("preferred_username") or
        response.get("given_name") or
        response.get("name") or
        details.get("username") or
        details.get("first_name")  # just in case
    )

    if nickname:
        username = nickname.lower().replace(" ", "")
        details["username"] = username
        print(f"Using nickname: {username}")
    else:
        print("Nickname not found")