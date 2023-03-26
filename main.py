from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/search")
def search():
    base_url = "https://dev.ylytic.com/ylytic/test"
    search_params = {}
    for param in request.args:
        search_params[param] = request.args[param]
    response = requests.get(base_url, params=search_params)
    comments = response.json()
    filtered_comments = []
    for comment in comments:
        # Filter comments based on search parameters
        if (
            "search_author" in request.args
            and request.args["search_author"] not in comment["author"]
        ):
            continue
        if "at_from" in request.args and comment["at"] < request.args["at_from"]:
            continue
        if "at_to" in request.args and comment["at"] > request.args["at_to"]:
            continue
        if "like_from" in request.args and comment["like"] < int(
            request.args["like_from"]
        ):
            continue
        if "like_to" in request.args and comment["like"] > int(request.args["like_to"]):
            continue
        if "reply_from" in request.args and comment["reply"] < int(
            request.args["reply_from"]
        ):
            continue
        if "reply_to" in request.args and comment["reply"] > int(
            request.args["reply_to"]
        ):
            continue
        if (
            "search_text" in request.args
            and request.args["search_text"] not in comment["text"]
        ):
            continue
        filtered_comments.append(comment)
    return jsonify(filtered_comments)


if __name__ == "__main__":
    app.run()
