from time import sleep
from datetime import datetime
from twitter_client import TwitterClient
from config import COMPARE_FOLLOWERS_SLEEP_INTERVAL
from slack_client import send_message_to_channel


if __name__ == '__main__':
    user_names_to_monitor = ["uncle__istvan", "schmetterlieb"]
    while True:

        for user_name in user_names_to_monitor:
            try:
                print(f"Refreshing data for {user_name}")
                # TODO: handle authorization error
                twitter_client = TwitterClient(user_name)
                unfollower_ids, new_follower_ids, followers_count = twitter_client.compare_followers_ids()
                print(f"followers count: {followers_count}")
                if unfollower_ids:
                    unfollower_names = twitter_client.get_names_from_ids(unfollower_ids)
                    # TODO: log and slack
                    print(f"[username] unfollowed by: {unfollower_names[]}")
                    send_message_to_channel(f"[{user_name}] unfollowed by: {unfollower_names[]}")

                # if new_follower_ids:
                #     new_follower_names = twitter_client.get_names_from_ids(new_follower_ids)
                #     send_message_to_channel(f"[username] followed by: {new_follower_names[:10]}")

                if not unfollower_ids and not new_follower_ids:
                    # print(f"no changes for {datetime.now()}\n")
                    pass
            except Exception as ex:
                send_message_to_channel(f"Error while processing {user_name}: {ex}")

        print(f"Taking a nap, back in {COMPARE_FOLLOWERS_SLEEP_INTERVAL} seconds\n\n")
        sleep(COMPARE_FOLLOWERS_SLEEP_INTERVAL)
