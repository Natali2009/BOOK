from ext import app

if __name__ == '__main__':
    from routes import home, register, login, add_book, test, booklight, brillant, saved, author_detail, book_detail, delete_book, logout, add_author, add_to_cart, checkout, cart, books_by_genre, books_by_emotion, add_to_favorites, remove_from_favorites, remove_from_cart
    app.run(debug=True)

