from django.shortcuts import render, redirect
from .models import BookModel
from _json import encode_basestring_ascii as c_encode_basestring_ascii
import requests
#fields of the book data to expand in template
fields = ['volumeInfo', 'saleInfo', 'accessInfo', 'searchInfo']

#getting json from the googleapi url
def get_json(url):
    res = requests.get(url).json()
    #check if query returned any values
    if 'items' in res.keys():
        return res['items']
    else:
        #else return empty dictionary
        print('No items returned')
        return dict()

#uploading hobbit books to database to initialize the database on the beginning
def initialize_database(request):
    url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
    objs = get_json(url)
    #update or create an object in a book db and  avoid duplication of books as it is in the source
    for obj in objs:
        exists = BookModel.objects.filter(data__id=obj['id'])
        if not exists:
            BookModel.objects.create(data=obj)
        else:
            book = BookModel.objects.get(data__id=obj['id'])
            book.data = obj
            book.save()
    return redirect('/home/books')

# GET /books
def get_books(request):
    books = BookModel.objects.all()
    return render(request, 'content.html', {'books': books, 'fields': fields})

#GET /books?published_date=????-??-??
def get_books_by_published_date(request, published_date):
    published_date=str(published_date)
    books = BookModel.objects.filter(data__volumeInfo__publishedDate__icontains=published_date)
    return render(request, 'content.html', {'books': books, 'fields': fields})

#GET /books?sort=published_date/-published_date
def get_books_sorted_by_published_date(request, sort):  
    if(sort=='-published_date'):
        books = BookModel.objects.all().order_by('-data__volumeInfo__publishedDate')
        return render(request, 'content.html', {'books': books, 'fields': fields})
    elif(sort=='published_date'):
        books = BookModel.objects.all().order_by('data__volumeInfo__publishedDate')
        return render(request, 'content.html', {'books': books, 'fields': fields})
    else: return redirect('/home/books')

#GET /books?authors="???????"
def get_books_by_author(request, authors):
    books=[]
    for author in authors:
        #cleaning string from ""
        author=author.replace('"', '')
        books+=BookModel.objects.filter(data__volumeInfo__authors__icontains=c_encode_basestring_ascii(author))
    return render(request, 'content.html', {'books': books, 'fields': fields})

#GET /books/<bookId>
def get_book_by_id(request, id):
    books=BookModel.objects.filter(data__id=id)
    return render(request, 'content.html', {'books': books, 'fields': fields})

#GET /books extension for redirecting paths to the adequate functions
def books_extension(request):
    published_date = request.GET.get('published_date')
    authors = request.GET.getlist('author')
    sort = request.GET.get('sort')
    if published_date: return(get_books_by_published_date(request, published_date))
    elif authors: return(get_books_by_author(request, authors))
    elif sort: return(get_books_sorted_by_published_date(request, sort))
    else: return(get_books(request))

#POST /db get query from the post method body and try to fetch the data form the url
def db_query(request, query):
    if query:
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + query
        objs = get_json(url)
        #update or create an object in a book db and  avoid duplication of books as it is in the source
        for obj in objs:
            exists = BookModel.objects.filter(data__id=obj['id'])
            if not exists:
                BookModel.objects.create(data=obj)
            else:
                book = BookModel.objects.get(data__id=obj['id'])
                book.data = obj
                book.save()
        return redirect('/home/books')
        
    else: return redirect('/home/db')

#GET /db
def db(request):
    if request.method=='GET':
        return render(request, 'db.html')
    elif request.method=='POST':
        return(db_query(request, request.POST.get('q', '')))
    else:
        return render(request, 'db.html')