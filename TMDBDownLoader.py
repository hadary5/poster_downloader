import requests
from config import TMDB_API_Key_v3_auth
import imdb

def size_str_to_int(x:str)->int:
    """sorting function to get the biggest picture size """
    return float("inf") if x == 'original' else int(x[1:])

class TMDBDownloader:
    def __init__(self):
        self.CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
        self.base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/'

        self.IMG_PATTERN = ''
        self.KEY = TMDB_API_Key_v3_auth
        self.url = self.CONFIG_PATTERN.format(key=self.KEY)
        self.config = requests.get(self.url).json()
        #print(self.config)
        self.base_url = self.config['images']['base_url']
        self.sizes = self.config['images']['poster_sizes']
        self.max_size = max(self.sizes, key=size_str_to_int) #use the sort function in max to get biggest size
    def getIMDBID(self,name):
        # creating instance of IMDb
        ia = imdb.IMDb()
        search = ia.search_movie(name)
        return "tt"+str(search[0].movieID)

    def getPoster(self,imdbid):
        self.IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'

        api_response =  requests.get(self.IMG_PATTERN.format(key=self.KEY, imdbid=imdbid)).json()
        posters = api_response['posters']
        poster_urls = []
        for poster in posters:
            rel_path = poster['file_path']
            url = "{0}{1}{2}".format(self.base_url, self.max_size, rel_path)
            poster_urls.append(url)
#########single poster dowload
        print(poster_urls)
        r = requests.get(poster_urls[0])
        nr=0
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(nr + 1, filetype)
        with open(filename, 'wb') as w:
            w.write(r.content)

        # for nr, url in enumerate(poster_urls):
        #     r = requests.get(url)
        #     filetype = r.headers['content-type'].split('/')[-1]
        #     filename = 'poster_{0}.{1}'.format(nr + 1, filetype)
        #     with open(filename, 'wb') as w:
        #         w.write(r.content)
        return poster_urls


if __name__ == "__main__":
    TMDBconn=TMDBDownloader()
    imdb_id=TMDBconn.getIMDBID("avengers")
    print(imdb_id)
    response=TMDBconn.getPoster(imdb_id)
    #print(response)

    print("hi")
