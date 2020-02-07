import datetime
from sqlalchemy import func

from model import connect_to_db, db, User, Item, Category

from server import app


def load_users():
    """Load sample users into database."""

    jess = User(email="jess@gmail.com", password="jess123")
    matt = User(email="jess@gmail.com", password="matt123")

    db.session.add(jess)
    db.session.add(matt)

    db.session.commit()


def load_items():
    """Load sample items into database."""

    # item_1 = Item(user_id="1", name="Blue Shirt", category_id="1", quantity=1, size="S", sold=False, sold_price =None, shipping_price=None)
    # item_2 = Item(user_id="2", name="Red Shirt", category_id="1", quantity=1, size="M", sold=True, sold_price =15, shipping_price=2)
    # item_3 = Item(user_id="1", name="Yellow Shirt", category_id="1", quantity=1, size="L", sold=True, sold_price =9, shipping_price=5)
    # item_4 = Item(user_id="2", name="Pink Shirt", category_id="1", quantity=1, size="XL", sold=False, sold_price =None, shipping_price=None)

    item_1 = Item(user_id=1, name="Blue Shirt", category_id=1)
    item_2 = Item(user_id=2, name="Red Shirt", category_id=1)
    item_3 = Item(user_id=1, name="Yellow Shirt", category_id=1)
    item_4 = Item(user_id=2, name="Pink Shirt", category_id=1)

    db.session.add(item_1)
    db.session.add(item_2)
    db.session.add(item_3)
    db.session.add(item_4)

    db.session.commit()

def load_categories():
    """Load sample categories into database."""

    category_1 = Category(category_name="Clothes")
    category_2 = Category(category_name="Accessories")

    db.session.add(category_1)
    db.session.add(category_2)
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.drop_all() #prevents dupe seeding
    db.create_all()

    load_users()
    load_categories()
    load_items()
    
