from MongoDBDAL import MongoDBDAL
import config
from TMDBDownLoader import TMDBDownloader

from flask import Flask, request, json, Response, render_template, make_response
#from pymongo import MongoClient
import logging as log

app = Flask(__name__)
##when connecting from docker use host name from docker compose
#mdb = MongoDBDAL("localhost", 27017, "movies")
mdb = MongoDBDAL("db_host", 27017, "movies")
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
        movie_name = request.form['name']
        imdb_id, file_name=TMDB.search_and_download(movie_name)
        mdb.write_image_file(config.content_temp_path + file_name,movie_name,imdb_id)
        return render_template('new_form.html', data=movie_name)
    return render_template('new_form.html')

########### mongo crud api ###############
@app.route('/mongo/<search_string>', methods=['GET'])
def read(search_string):
    print (search_string)
    binary_file=mdb.read_image_file(search_string)
    #file_name="./"+search_string+".jpeg"
    #return render_template("image_response.html", user_image=file_name)
    response = make_response(binary_file)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % search_string)
    return response


@app.route('/mongo/<search_string>', methods=['DELETE'])
def mongo_delete(search_string):
    data = search_string
    if not data :
        return Response(response=json.dumps({"Error": "Please provide movie name"}),
                        status=400,
                        mimetype='application/json')
    response=mdb.del_image_file(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)