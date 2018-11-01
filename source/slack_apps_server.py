from flask import Flask, request, Response


slack_apps_server = Flask(__name__)


@slack_apps_server.route('/', methods=["POST", "GET"])
def test_endpoint():
    if request.method == "POST":
        print(request.data)
        return Response(request.data)

    if request.method == "GET":
        print("/slack endpoint online")
        return Response("/slack endpoint online")


if __name__ == "__main__":
    slack_apps_server.run(debug=True)
