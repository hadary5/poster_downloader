from MongoDBDAL import MongoDBDAL
import config
from TMDBDownLoader import TMDBDownloader

from flask import Flask, request, json, Response
#from pymongo import MongoClient
import logging as log
