from flask import current_app as app

@app.route("/", methods=["GET", "POST"])
def indexMain():


  return "hi", 200