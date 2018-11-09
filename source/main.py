from time import sleep
from datetime import datetime
from twitter_client import TwitterClient
from config import COMPARE_FOLLOWERS_SLEEP_INTERVAL
from utils import log_and_slack


if __name__ == '__main__':
    user_names_to_monitor = ["uncle__istvan", "schmetterlieb"]
    while True:
        for user_name in user_names_to_monitor:
            try:
                print(f"[{datetime.now()}] Refreshing data for {user_name}")

                # TODO: handle authorization error
                twitter_client = TwitterClient(user_name)
                unfollower_ids, new_follower_ids, followers_count = twitter_client.compare_followers_ids()

                # new unfollowers
                if unfollower_ids:
                    unfollower_names = twitter_client.get_names_from_ids(unfollower_ids)

                    # TODO: send to different channels / show avatar
                    log_and_slack(f"@{user_name} unfollowed by: {unfollower_names}")

                # new followers
                if new_follower_ids:
                    pass

                # no changes
                if not unfollower_ids and not new_follower_ids:
                    pass

            except Exception as ex:
                log_and_slack(f"Error while processing {user_name}: {ex}")

        print(f"Taking a nap, back in {COMPARE_FOLLOWERS_SLEEP_INTERVAL} seconds\n\n")
        sleep(COMPARE_FOLLOWERS_SLEEP_INTERVAL)
