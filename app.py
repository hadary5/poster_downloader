from MongoDBDAL import MongoDBDAL
import config
from TMDBDownLoader import TMDBDownloader

from flask import Flask, request, json, Response,render_template
#from pymongo import MongoClient
import logging as log

app = Flask(__name__)
mdb = MongoDBDAL("localhost", 27017, "movies")
TMDB = TMDBDownloader()
#    TMDB.search_and_download(movie_name)


@app.route('/')
def index():
    return '<h1>Hello  Class</h1>'


@app.route('/user/<name>')
def user(name):
    return f'<h1>Hello, {name}!</h1>'


@app.route('/search', methods=['GET', 'POST'])  # GET REQUEST
def load_insert_item_html():
    if request.method == 'POST':
        print("test")
        movie_name = request.form['name']
        imdb_id, file_name=TMDB.search_and_download(movie_name)
        mdb.write_image_file(config.content_temp_path + file_name,movie_name,imdb_id)
        print(movie_name)
        return render_template('new_form.html', data=movie_name)
    return render_template('new_form.html')

########### mongo crud api ###############
@app.route('/mongo/<search_string>', methods=['GET'])
def read(search_string):
    mdb.read_image_file(search_string)







if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)