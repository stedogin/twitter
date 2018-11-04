from slack_apps_server import slack_apps_server


slack_apps_server.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)

