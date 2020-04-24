import re
import traceback
from bookdb import BookDB

DB = BookDB()

def resolve_path(path):
    funcs = {'': books, 'book': book}

    path = path.strip('/').split('/')
    args = path[1:]
    
    try:
        func_name = funcs[path[0]]
    except KeyError:
        raise NameError

    return func_name, args


def book(book_id):
    page = """
        <h1>{title}</h1>
        <b>Author</b>  {author}</br>
        <b>Publisher</b> {publisher}</br>
        <b>ISBN</th><td> {isbn}</br>
        <a href="/">Back to the list</a>
    """
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    return page.format(**book)

def books():
    _template = "<li><a href='/book/{id}'>{title}</a></li>"
    body = [ "<h1>My Bookshelf</h1>", "<ul>" ]
    [ body.append(_template.format(**title_dict)) for title_dict in DB.titles() ]

    return '\n'.join(body)


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    status = "200 OK"
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>" 
        print(traceback.format_exc())
    finally:
        headers.append(('Content-Length', str(len(body))))
        start_response(status, headers)
    return [body.encode('utf8')]
       

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
