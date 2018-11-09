from slack_app_client import SlackAppClient

slack_client = SlackAppClient()


def log_and_slack(message):
    print(message)
    slack_client.send_message_to_channel(message)
