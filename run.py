
from livereload import Server
from app import app

app.debug = True
server = Server(app=app.wsgi_app)
server.serve()

