#gunicorn sse:app --worker-class gevent --bind 0.0.0.0:5000
#gunicorn sse:app -k gevent -b 0.0.0.0:50
#nohup mongod &
#nohup redis-server /etc/redis/redis.conf &
gunicorn hemera:app -k gevent -b 0.0.0.0:5000
#nohup gunicorn -b 0.0.0.0:80 -k eventlet -w 40 -t 99999 run:app &

#hello world
