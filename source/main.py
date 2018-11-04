from time import sleep
from datetime import datetime
from twitter_client import TwitterClient
from config import COMPARE_FOLLOWERS_SLEEP_INTERVAL
from slack_client import send_message_to_channel


if __name__ == '__main__':
    user_names_to_monitor = ["uncle__istvan", "schmetterlieb"]
    while True:
        for user_name in user_names_to_monitor:
            print(f"Refreshing data for {user_name}")
            # TODO: handle authorization error
            twitter_client = TwitterClient(user_name)
            unfollower_ids, new_follower_ids = twitter_client.compare_followers_ids()

            # TODO: merge, get names from ids

            if unfollower_ids:
                unfollower_names = twitter_client.get_names_from_ids(unfollower_ids)
                # TODO: slack
                send_message_to_channel(f"UNFOLLOWERS: {unfollower_names[:10]}")

            if new_follower_ids:
                new_follower_names = twitter_client.get_names_from_ids(new_follower_ids)

                # TODO: slack
                send_message_to_channel(f"NEW FOLLOWERS: {new_follower_names[:10]}")

            if not unfollower_ids and not new_follower_ids:
                print(f"no changes for {datetime.now()}")

        print(f"Taking a nap, back in {COMPARE_FOLLOWERS_SLEEP_INTERVAL} seconds")
        sleep(COMPARE_FOLLOWERS_SLEEP_INTERVAL)
