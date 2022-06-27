#!/usr/bin/env python3

import zulip
import pprint
import sys
# client = zulip.Client(config_file="~/yzulipterminal/roles/member/zuliprc")
client = zulip.Client(config_file="~/zuliprc")

# Register the queue
# result = client.register(
#     event_types=["subscription"],
# )
# result = client.remove_subscriptions(
#     ["test here"],
# )

# subscribed_streams = result["subscriptions"]
# for stream_in_subscriptions in subscribed_streams:
#     print(stream_in_subscriptions["name"])

# result = client.remove_subscriptions(
#     [""],
# )

# ------------------------------------------------------------------------
# call_on_each_event()

# Print every message the current user would receive
# This is a blocking call that will run forever
# client.call_on_each_message(lambda msg: sys.stdout.write(str(msg) + "\n"))

# Print every event relevant to the user
# This is a blocking call that will run forever
# client.call_on_each_event(lambda event: sys.stdout.write(str(event) + "\n"))

# Register the queue
# result = client.register(
#     event_types=["subscriptions"],
# )

# pprint.pprint(result)
