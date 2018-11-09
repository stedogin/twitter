import hmac
from hashlib import sha256
from urllib.parse import urlencode
from slackclient import SlackClient
from python_utils import get_environment_variable
from config import DEFAULT_SLACK_CHANNEL_ID, DEFAULT_SLACK_ICON


class SlackAppClient:
    def __init__(self):
        self.slack_oauth_access_token = get_environment_variable("SLACK_OAUTH_ACCESS_TOKEN")
        self.validation_hash_key = get_environment_variable("SLACK_SIGNING_SECRET")

        self.slack_client = SlackClient(self.slack_oauth_access_token)

    def get_channel_ids_by_names(self):
        api_call_result = self.slack_client.api_call(method="channels.list")
        channel_ids_by_names = {}
        if api_call_result["ok"]:
            channels_data = api_call_result["channels"]
            channel_ids_by_names = {channel["name"]: channel["id"] for channel in channels_data
                                    if not channel["is_archived"]}
        return channel_ids_by_names

    def get_channel_id_from_name(self, channel_name):
        channel_ids_by_names = self.get_channel_ids_by_names()
        channel_id = channel_ids_by_names[channel_name]
        return channel_id

    def send_message_to_channel(self, message="ping", attachments=None, channel_id=DEFAULT_SLACK_CHANNEL_ID,
                                icon=DEFAULT_SLACK_ICON, display_name=None):
        result = self.slack_client.api_call(method="chat.postMessage",
                                            text=message,
                                            attachments=attachments,
                                            icon_emoji=icon,
                                            channel=channel_id,
                                            username=display_name)
        return result

    def is_valid_request(self, request):
        request_body = urlencode(request.form)
        request_headers = request.headers
        request_timestamp = str(request_headers["X-Slack-Request-Timestamp"])
        request_signature = request_headers["X-Slack-Signature"]
        request_version, _ = str(request_signature).split('=')

        # TODO: validate recent timestamp for replay attacks

        validation_hash_message = "v0:" + request_timestamp + ':' + request_body
        validation_hash_key = self.validation_hash_key
        validation_hexdigest = hmac.new(key=str.encode(validation_hash_key),
                                        msg=str.encode(validation_hash_message), digestmod=sha256).hexdigest()
        validation_result = f"{request_version}={validation_hexdigest}"

        return hmac.compare_digest(validation_result, request_signature)
