from typing import Any, Optional

import logging
import os.path
import random
import time

import httplib2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from storytime.story import get_save_path, load_from_json

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of
# access. If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, OSError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def get_authenticated_service() -> Optional[Any]:
    """Get a valid user credentials from storage if available and returns
    a YouTube service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        return build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=creds
        )
    except HttpError as err:
        logger.error(err)


def resumable_upload(insert_request):
    """This method implements an exponential backoff strategy to resume a
    failed upload."""
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            logger.info("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if "id" in response:
                    logger.info(
                        f"Video id '{response['id']}' was successfully "
                        f"uploaded."
                    )
                else:
                    exit(
                        f"The upload failed with an unexpected response: "
                        f"{response}"
                    )
        except HttpError as hte:
            if hte.resp.status in RETRIABLE_STATUS_CODES:
                error = (
                    f"A retriable HTTP error {hte.resp.status} "
                    f"occurred:\n{hte.content}"
                )
            else:
                raise
        except RETRIABLE_EXCEPTIONS as re:
            error = f"A retriable error occurred: {re}"

        if error is not None:
            logger.error(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2**retry
            sleep_seconds = random.random() * max_sleep
            logger.info(
                f"Sleeping {sleep_seconds} seconds and then " f"retrying..."
            )
            time.sleep(sleep_seconds)


def initialize_upload(
    youtube,
    video_file: str,  # Video file to upload
    title: Optional[str] = "Test Title",  # Video title
    description: Optional[str] = "Test Description",  # Video description
    tags: Optional[list] = None,
    category: Optional[int] = 24,  # Numeric video category. Default to
    # 24 = Entertainment. See
    # https://developers.google.com/youtube/v3/docs/videoCategories/list
    privacy_status: Optional[str] = "private",
) -> None:
    """Uploads a video to YouTube and optionally sets the video's title,
    description, and category."""

    body = dict(
        snippet=dict(
            title=title,
            description=description,
            tags=tags,
            categoryId=category,
        ),
        status=dict(privacyStatus=privacy_status),
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a
        # lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the
        # entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True),
    )

    resumable_upload(insert_request)


if __name__ == "__main__":
    youtube_service = get_authenticated_service()
    story = load_from_json(
        os.path.join(get_save_path(), "TorysJourneyofLoveandFriendship.json")
    )
    video = os.path.join(
        get_save_path(), "Tory's Journey of Love and Friendship.mp4"
    )
    try:
        initialize_upload(
            youtube_service,
            video_file=video,
            title=story.title,
            description=story.synopsis,
        )
    except HttpError as he:
        logger.error(f"An HTTP error {he.resp.status} occurred:\n{he.content}")
