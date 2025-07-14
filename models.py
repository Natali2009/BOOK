from ext import db, login_manager
from flask_login import UserMixin

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class Book(db.Model, BaseModel, UserMixin):

    __tablename__ = "books"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), default="default_image.png")
    genre = db.Column(db.String(), nullable=False)
    time = db.Column(db.String(), nullable=False)
    character = db.Column(db.String(), nullable=False)
    ending = db.Column(db.String(), nullable=False)
    purpose = db.Column(db.String(), nullable=False)
    is_brillant = db.Column(db.Boolean, default=False)
    emotion = db.Column(db.String(), nullable=False)

class Author(db.Model, BaseModel, UserMixin):

    __tablename__ = "authors"


    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    bio = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(), default="default_image.png")


class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "users"


    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    image = db.Column(db.String(), default="profile.jpg")
    role = db.Column(db.String())

class Favorite(db.Model, BaseModel,  UserMixin):

    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer(), db.ForeignKey("books.id"))

    user = db.relationship("User", backref="favorites")
    book = db.relationship("Book", backref="favorites")

class CartItem(db.Model):

    __tablename__ = "cart_items"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer(), db.ForeignKey("books.id"))
    quantity = db.Column(db.Integer(), default=1,  nullable=False )

    user = db.relationship("User", backref="cart_items")
    book = db.relationship("Book", backref="in_carts")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)