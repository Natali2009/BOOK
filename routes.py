from ext import app, db
from flask import render_template, redirect, flash, request
from forms import RegisterForm, LoginForm, AddBookForm, AddAuthorForm, TestForm
from os import path
from models import Book, Author, User, Favorite, CartItem
from flask_login import login_user, logout_user, login_required, current_user
import random


@app.route('/')
def home():
    books = Book.query.all()
    authors = Author.query.all()
    return render_template('home.html', books=books, authors=authors)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data).first():
            flash('ეს მომხმარებლის სახელი უკვე დაკავებულია. სცადეთ სხვა.', 'warning')
            return render_template('register.html', form=form)

        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        image = form.profile_img.data
        if image:
            image.save(f"{app.root_path}/static/images/{image.filename}")
            new_user.image = image.filename
        else:
            new_user.image = "profile.jpg"

        new_user.create()
        flash('რეგისტრაცია წარმატებით დასრულდა! გთხოვთ, შეხვიდეთ სისტემაში.', 'success')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.username.data == User.username).first()
        if user:
            login_user(user)
            flash(" შენ წარმატებით გაიარე ავტორიზაცია", 'success')
            return redirect("/")
        else:
            flash("მომხმარებელი არ მოიძებნა ან პაროლი არასწორია")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_book', methods=["GET", "POST"])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(name=form.name.data,
                        price=form.price.data,
                        author=form.author.data,
                        description=form.description.data,
                        genre=form.genre.data,
                        time=form.time.data,
                        character=form.character.data,
                        ending=form.ending.data,
                        purpose=form.purpose.data,
                        is_brillant=form.is_brillant.data,
                        emotion=form.emotion.data
                        )

        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_book.image = image.filename

        Book.create(new_book)

        flash('წიგნი წარმატებით დაემატა!', 'success')
    role = current_user.role
    return render_template('add_book.html', form=form, role=role)


@app.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = AddAuthorForm()
    if form.validate_on_submit():
        new_author = Author(name=form.name.data, bio=form.bio.data)

        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_author.image = image.filename

        new_author.create()
        flash("ავტორი წარმატებით დაემატა!", "success")
        return redirect('/')
    role = current_user.role
    return render_template('add_author.html', form=form, role=role)


@app.route('/genre/<string:genre_name>')
def books_by_genre(genre_name):
    books = Book.query.filter(Book.genre == genre_name).all()
    return render_template("books_by_filter.html", books=books, filter_name=genre_name, filter_type="ჟანრი")


@app.route('/emotion/<string:emotion_name>')
def books_by_emotion(emotion_name):
    books = Book.query.filter(Book.emotion == emotion_name).all()
    return render_template("books_by_filter.html", books=books, filter_name=emotion_name, filter_type="ემოცია")


@app.route('/book_detail/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get(book_id)
    author = Author.query.filter(Author.name==book.author).first()
    return render_template('book_detail.html', book=book, author_obj=author)


@app.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    Book.delete(book)
    flash('წიგნი წარმატებით წაიშალა!', 'success')
    role = current_user.role
    return render_template('home.html', role=role)


@app.route('/author/<int:author_id>')
@login_required
def author_detail(author_id):
    author = Author.query.get(author_id)
    return render_template("author_detail.html", author=author)


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    form = TestForm()
    book = None
    message = None

    if request.method == 'POST':
        if form.validate_on_submit():
            book = Book.query.filter(
                Book.genre == form.genre.data,
                Book.time == form.time.data,
                Book.character == form.character.data,
                Book.ending == form.ending.data,
                Book.purpose == form.purpose.data
            ).first()

            if not book:
                books = Book.query.all()
                if books:
                    book = random.choice(books)
                    message = "სამწუხაროდ, ზუსტი რეკომენდაცია ვერ მოიძებნა, მაგრამ გირჩევთ გადახედოთ მოცემულ წიგნს..."
            return render_template('test_result.html', book=book, message=message)

        message = "გთხოვთ, ყველა კითხვა შეავსოთ შედეგის მისაღებად."

    return render_template('test.html', form=form, message=message)


@app.route('/test_result')
def test_result():
    return render_template('test_result.html')


@app.route('/booklight')
def booklight():
    return render_template('booklight.html')


@app.route('/brillant')
def brillant():
    books = Book.query.filter(Book.is_brillant == True).all()
    return render_template('brillant.html', books=books)


@app.route('/saved')
@login_required
def saved():
    favorites = Favorite.query.filter(Favorite.user_id == current_user.id).all()
    saved_books = [fav.book for fav in favorites]
    return render_template('saved.html', saved_books=saved_books)


@app.route('/add_to_favorites/<int:book_id>', methods=['POST'])
@login_required
def add_to_favorites(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("წიგნი ვერ მოიძებნა", "danger")
        return redirect("/")

    existing_fav = Favorite.query.filter(
        Favorite.user_id == current_user.id,
        Favorite.book_id == book_id
    ).first()

    if not existing_fav:
        favorite = Favorite(user_id=current_user.id, book_id=book_id)
        db.session.add(favorite)
        db.session.commit()
        flash('წიგნი დაემატა რჩეულებში!', 'success')
    else:
        flash('ეს წიგნი უკვე შენახულია.', 'info')
    author_obj = Author.query.filter(Author.name==book.author).first()
    return render_template('book_detail.html', book=book, author_obj=author_obj)


@app.route('/remove_from_favorites/<int:book_id>', methods=["POST"])
@login_required
def remove_from_favorites(book_id):
    favorite = Favorite.query.filter(
        Favorite.user_id == current_user.id,
        Favorite.book_id==book_id
    ).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash("წიგნი წაიშალა შენახულებიდან.", "success")
    else:
        flash("წიგნი შენახულებში ვერ მოიძებნა.", "warning")
    return redirect("/saved")


@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter(CartItem.user_id == current_user.id).all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total_price)


@app.route("/add_to_cart/<int:book_id>", methods=['POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get(book_id)
    existing_item = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.book_id == book_id
    ).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=current_user.id, book_id=book_id)
        db.session.add(new_item)
    db.session.commit()
    flash("წიგნი წარმატებით დაემატა კალათაში.")
    author_obj = Author.query.filter(Author.name == book.author).first()
    return render_template("book_detail.html", book=book,  author_obj=author_obj)


@app.route('/remove_from_cart/<int:book_id>', methods=["POST"])
@login_required
def remove_from_cart(book_id):
    item = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.book_id == book_id
    ).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("წიგნი წაიშალა კალათიდან.", "success")
    else:
        flash("წიგნი ვერ მოიძებნა კალათაში.", "warning")
    return redirect("/cart")


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        cart_items = CartItem.query.filter(CartItem.user_id == current_user.id).all()
        if not cart_items:
            return redirect("/")

        for item in cart_items:
            db.session.delete(item)
        db.session.commit()

        flash("გადახდა წარმატებით შესრულდა. მადლობა შენაძენისთვის!")
        return redirect("/")

    return render_template("checkout.html")
