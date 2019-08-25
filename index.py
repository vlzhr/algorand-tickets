from flask import Flask, render_template, request, redirect, url_for
from algodata_handler import store_purchase, event_by_id, read_events, add_event

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template("index.html", events=read_events())


@app.route("/eventform")
def event_form():
    return render_template("eventform.html", url_for=url_for, event=event_by_id(request.args.get("eid", 1)))


@app.route("/add_purchase")
def add_purchase():
    r = request.args
    txid = store_purchase(event_by_id(r["eid"]), {"name": r["name"], "email": r["email"], "ticket_type": r["type"]})
    return redirect("congrats?txid="+txid)


@app.route("/congrats")
def congrats():
    return render_template("congrats.html", txid=request.args["txid"])


@app.route("/create_event")
def create_event():
    return render_template("creating.html", event=add_event(request.args["name"]))


if __name__ == "__main__":
    app.run()
