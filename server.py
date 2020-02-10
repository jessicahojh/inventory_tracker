from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Item, Category

import requests

import json

from datetime import datetime

app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Process Registration."""

    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password, status=status)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/login', methods=['GET'])
def login_form():
    """Login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect(f"/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route('/')
def homepage():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/items")
def items_list():
    """Show list of items."""

    item = Item.query.all()

    return render_template("items.html", item=item)


@app.route('/additems', methods=['GET'])
def add_item():
    """Show form for adding item."""

    return render_template("add_item.html")

@app.route("/additems", methods=['POST'])
def add_item_process():
    """If user is logged in, let them add items to their inventory. Users can only see the 
    option to add inventory if they are logged in"""

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    name = request.form["name"]
    category_id = request.form["category_id"]
    quantity = request.form["quantity"]
    size = request.form["size"]
    sold = request.form["sold"]
    sold_price = request.form["sold_price"]
    shipping_price = request.form["shipping_price"]


    new_item = Item(user_id=user_id, name=name, category_id=category_id, quantity=quantity,
    size=size,sold=sold, sold_price=sold_price, shipping_price=shipping_price)

    db.session.add(new_item)
    db.session.commit()

    return redirect("/items")
    
    
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
    # app.run(host="0.0.0.0")