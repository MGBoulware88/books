from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask_app.models import author

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']   
        self.num_of_pages = data['num_of_pages']
        self.favorited_by = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books"

        results = connectToMySQL(DB).query_db(query)
        
        new_list = []
        
        for row in results:
            new_list.append(cls(row))
        print(new_list)
        return new_list
    
    # @classmethod
    # def get_non_favorite_books(cls, data):
    #     query = "SELECT * FROM books WHERE NOT id = ();"

    #     results = connectToMySQL(DB).query_db(query)
        
    #     new_list = []
        
    #     for row in results:
    #         new_list.append(cls(row))
    #     print(new_list)
    #     return new_list

    @classmethod
    def get_book_by_id(cls, id):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        data = {
            'id':id
        }
        results = connectToMySQL(DB).query_db(query, data)
        print(f"book by id: {results[0]}")
        return results[0]
    
    @classmethod
    def get_book_and_favorited_by(cls, id):
        query = "SELECT * from books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        data = {
            'id':id
        }
        results = connectToMySQL(DB).query_db(query, data)
        print(results)
        new_book = cls(results[0])
        for row in results:
            authors_who_favorited = {
                'id':row['authors.id'],
                'name':row['name'],
                'num_of_pages':row['num_of_pages'],
                'created_at':row['authors.created_at'],
                'updated_at':row['authors.updated_at']
            }
            new_book.favorited_by.append(author.Author(authors_who_favorited))
        return new_book
    
    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES(%(title)s, %(num_pages)s);"
        results = connectToMySQL(DB).query_db(query, data)
        print(f"results: {results}")
        return results
    
    @classmethod
    def favorite_book(cls, data):
        query = "INSERT INTO favorites (book.id, author.id) VALUES(%(bid)s, %(aid)s);"
        results = connectToMySQL(DB).query_db(query, data)
        return results