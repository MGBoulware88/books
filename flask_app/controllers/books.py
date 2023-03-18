from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import author
from flask_app.models import book

@app.route("/books")
def show_books():
    books = book.Book.get_all_books()
    return render_template("books.html", books = books)

@app.route("/books/create", methods=["POST"])
def create_book():
    data = {
        'title':request.form['title'],
        'num_pages':request.form['num_pages']
    }

    book.Book.create_book(data)

    return redirect("/books")

@app.route("/books/<int:id>")
def books_show(id):
    new_book = book.Book.get_book_and_favorited_by(id)
    favorited_by = new_book.favorited_by
    all_authors = author.Author.get_all_authors()
    # print(f"THIS BOOK IS FAVORITED BY THESE AUTHORS: {favorited_by}")
    return render_template("books_show.html", book = new_book, authors = favorited_by, all_authors = all_authors)
    
@app.route("/books/<int:id>/favorite", methods=['POST'])
def favorite_book(id):
    data = {
        'book_id':id,
        'author_id':request.form['authordd']
    }
    
    author.Author.favorite_book(data)

    return redirect(f"/books/{id}")
