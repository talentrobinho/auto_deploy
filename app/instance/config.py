DEBUG = True
SECRET_KEY = 'development key'
EXPLAIN_TEMPLATE_LOADING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:////search/odin/flasky/app/data.sqlite'
JENKINS_URL = 'http://10.142.82.202:8080/jenkins/'
JENKINS_USERNAME = 'admin'
JENKINS_PASSWD = '6f4f8a926d37406da08c6ec92fd855e8'
SALTAPI_URL = 'http://10.142.83.181:8000/'
SALTAPI_USERNAME = 'saltapi'
SALTAPI__PASSWD = 'salt'
REDIS_URL = 'redis://localhost'
<<<<<<< HEAD

'''
    redis cache configure
'''
CACHE_TYPE = "redis"
CACHE_REDIS_HOST = "10.129.149.152"
CACHE_REDIS_PORT = "6379"
CACHE_REDIS_DB = 0
CACHE_REDIS_PASSWORD = ""
CACHE_REDIS_TIMEOUT = 60

'''
    redis privileges database configure
'''
PRIVILEGES_TYPE = "redis"
PRIVILEGES_REDIS_HOST = "10.129.149.152"
PRIVILEGES_REDIS_PORT = "6379"
PRIVILEGES_REDIS_DB = 1

'''
    super administrator list
'''
ADMIN_LIST = "lizhansheng songwanbo"
=======
>>>>>>> upstream/master
