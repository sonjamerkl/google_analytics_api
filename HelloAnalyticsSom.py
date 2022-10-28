"""A simple example of how to access the Google Analytics API."""

from pprint import pprint
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes
    )

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return (
        service.data()
        .ga()
        .get(
            ids="ga:" + profile_id,
            start_date="2022-06-01",
            end_date="2022-06-30",
            dimensions="ga:hostname",
            metrics="ga:pageviews",  # ga:sessionviews
        )
        .execute()
    )


def print_results(service, results):
    # Print data nicely for the user.
    service = service
    # Example #2:
    # Retrieves views (profiles) for all properties of the user's account,
    # using a wildcard '~all' as the webpropertyId.

    # profiles = (
    #     service.management()
    #     .profiles()
    #     .list(accountId="126693408", webPropertyId="~all")
    #     .execute()
    # )

    # Example #3:
    # The results of the list method are stored in the profiles object.
    # The following code shows how to iterate through them.
    # for profile in profiles.get("items", []):
    #     property_id = profile.get("webPropertyId")
    #     property_id_internal = profile.get("internalWebPropertyId")
    #     profile_id = profile.get("id")
    #     profile_name = profile.get("name")
    #     print("Property ID,Internal Property ID,View (Profile ID),View (Profile) Name")
    #     print(
    #         property_id
    #         + ","
    #         + property_id_internal
    #         + ","
    #         + profile_id
    #         + ","
    #         + profile_name
    #     )
    pprint(results)


def main():
    # Define the auth scopes to request.
    scope = "https://www.googleapis.com/auth/analytics.readonly"
    key_file_location = "client_secrets.json"
    profile_id = "190809828"

    # Authenticate and construct service.
    service = get_service(
        api_name="analytics",
        api_version="v3",
        scopes=[scope],
        key_file_location=key_file_location,
    )

    print_results(service, get_results(service, profile_id))


if __name__ == "__main__":
    main()
