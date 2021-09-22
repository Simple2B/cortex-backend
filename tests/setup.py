import os

os.environ["TESTING"] = "True"
if "FLASK_APP" in os.environ:
    del os.environ["FLASK_APP"]
