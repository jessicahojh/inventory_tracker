from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

class User(db.Model):
    """User accounts on the website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Category(db.Model):
    """Item categories."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)


class Item(db.Model):
    """User's items in their inventory."""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # created_date = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    # purchase_date = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    sold = db.Column(db.Boolean, default=False)
    sold_price = db.Column(db.Integer, default=0)
    shipping_price = db.Column(db.Integer, default=0)
    # sold_date = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


    # Define relationship to user
    user = db.relationship("User", backref=db.backref("items"))
    # Define relationship to category
    user = db.relationship("Category", backref=db.backref("items"))


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    #Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///inventory'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")