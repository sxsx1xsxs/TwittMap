from flask import Flask, request
from flask import render_template

application = Flask(__name__)


@application.route('/')
def search():
    return render_template("search.html")

# # run the app.
# if __name__ == "__main__":
#     # Setting debug to True enables debug output. This line should be
#     # removed before deploying a production app.
#     application.debug = True
#     application.run()

