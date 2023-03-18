from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import author
from flask_app.models import book

@app.route("/authors")
def show_authors():
    authors = author.Author.get_all_authors()
    return render_template("authors.html", authors = authors)

@app.route("/authors/create", methods=["POST"])
def create_author():
    data = {
        'name':request.form['name']
    }

    author.Author.create_author(data)

    return redirect("/authors")

@app.route("/authors/<int:id>")
def show_author(id):
    new_author = author.Author.get_author_and_favorite_books(id)
    fav_books = new_author.favorites
    all_books = book.Book.get_all_books()
    print(f"Favorite Books: {fav_books}")
    print(f"All Books: {all_books}")

    return render_template("authors_show.html", author=new_author, books=fav_books, all_books=all_books)
    
@app.route("/authors/<int:id>/favorite", methods=['POST'])
def add_favorite(id):
    data = {
        'author_id':id,
        'book_id':request.form['bookdd']
    }
    author.Author.favorite_book(data)
    
    return redirect(f"/authors/{id}")