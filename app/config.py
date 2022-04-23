from credintals import *

DEBUG = False
PORT = 8080
HOST ='0.0.0.0'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_POOL_PRE_PING = True
SQLALCHEMY_ENGINE_OPTIONS = {'pool_size' : 100, 'pool_recycle' : 280, 'pool_timeout' : 280,}