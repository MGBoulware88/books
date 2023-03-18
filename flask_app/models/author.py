from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.favorites = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors"

        results = connectToMySQL(DB).query_db(query)
        
        new_list = []
        
        for row in results:
            new_list.append(cls(row))
        return new_list
    
    @classmethod
    def get_author_by_id(cls, id):
        query = "SELECT * FROM authors WHERE id = %(id)s;"
        data = {
            'id':id
        }
        results = connectToMySQL(DB).query_db(query, data)
        print(f"author by id: {results[0]}")
        return results[0]
    
    @classmethod
    def get_author_and_favorite_books(cls, id):
        query = "SELECT * from authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        data = {
            'id':id
        }
        results = connectToMySQL(DB).query_db(query, data)
        print(results)
        new_author = cls(results[0])
        for row in results:
            fav_books = {
                'id':row['books.id'],
                'title':row['title'],
                'num_of_pages':row['num_of_pages'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at']
            }
            new_author.favorites.append(book.Book(fav_books))
        return new_author

    
    @classmethod
    def create_author(cls, data):
        query = "INSERT INTO authors (name) VALUES(%(name)s);"
        results = connectToMySQL(DB).query_db(query, data)
        print(f"results: {results}")
        return results
    
    @classmethod
    def favorite_book(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"


        results = connectToMySQL(DB).query_db(query, data)
        return results