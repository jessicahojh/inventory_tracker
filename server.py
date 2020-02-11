from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Item

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

    new_user = User(email=email, password=password)

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

# @app.route('/')
# def homepage():
#     """Homepage."""

#     return render_template("homepage.html")

@app.route('/')
def homepage():
    """Homepage."""

    return render_template("index.html", token="Hello Flask + React")

@app.route("/items")
def items_list():
    """Show list of items."""

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    item = Item.query.filter(Item.user_id == user_id).all()

    return render_template("items.html", item=item)

@app.route("/solditems")
def sold_items_list():
    """Show list of sold items."""

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    item = Item.query.filter(Item.user_id == user_id, Item.sold == True).all()

    return render_template("items.html", item=item)

@app.route("/items/<int:item_id>")
def specific_item(item_id):
    """Show specific item."""

    item = Item.query.get(item_id)

    return render_template("specific_item.html", item=item)

@app.route("/items/<int:item_id>/sold", methods=['GET'])
def sold_form(item_id):
    """Show sold form."""

    item = Item.query.get(item_id)

    return render_template("sold_form.html", item=item)

@app.route("/items/<int:item_id>/sold", methods=['POST'])
def sold_process(item_id):
    """Process sold item."""

    item = Item.query.get(item_id)

    sold_price = request.form["sold_price"]
    shipping_price = request.form["shipping_price"]

    item.sold = True
    item.sold_price = sold_price
    item.shipping_price = shipping_price

    db.session.commit()

    return redirect("/items")

@app.route("/items/<int:item_id>/edit", methods=['GET'])
def edit_form(item_id):
    """Show edit form."""

    item = Item.query.get(item_id)

    return render_template("edit_item.html", item=item)

@app.route("/items/<int:item_id>/edit", methods=['POST'])
def process_edit_form(item_id):
    """Process edit form."""

    item = Item.query.get(item_id)

    name = request.form["name"]
    quantity = request.form["quantity"]
    size = request.form["size"]

    item.name = name
    item.quantity = quantity
    item.size = size

    db.session.commit()

    return redirect("/items")

@app.route("/items/<int:item_id>/delete", methods=['POST'])
def delete(item_id):
    """Delete item."""

    # Doesn't work

    item = Item.query.get(item_id)

    db.session.delete(item)
    db.session.commit()

    return redirect("/")

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

    image = request.form["img"]
    name = request.form["name"]
    quantity = request.form["quantity"]
    size = request.form["size"]

    new_item = Item(user_id=user_id, name=name, image=image, quantity=quantity, size=size)

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