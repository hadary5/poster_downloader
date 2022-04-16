import os

import pymongo
import gridfs

class MongoDBDAL:

    def __init__(self,ip,port,db_name):
        self.client= pymongo.MongoClient(ip, port)
        self.database = self.client[db_name]
        # Create an object of GridFs for the above database.
        self.fs = gridfs.GridFS(self.database)

    def insert_image_file(self,file_name,movie_name,imdb_code):
        file = file_name
        head, tail = os.path.split(file_name)
        with open(file, 'rb') as f:
            current_image = f.read()
        self.fs.put(current_image, file_name=tail,movie_name=movie_name,imdb_code=imdb_code)

    def read_image_file(self,movie_name):
        file = self.fs.find_one({"movie_name": movie_name}).read()
        with open(movie_name+".jpeg", 'wb') as w:
            w.write(file)


if __name__ == "__main__":
    mdb=MongoDBDAL("localhost",27017,"movies")
    content_temp_path="./temp_content/"

    mdb.insert_image_file(content_temp_path+"poster_spiderman.jpeg","spiderman","tt0145487")
    mdb.read_image_file("spiderman")

