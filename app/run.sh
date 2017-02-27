#gunicorn sse:app --worker-class gevent --bind 0.0.0.0:5000
#gunicorn sse:app -k gevent -b 0.0.0.0:50
#nohup mongod &
#nohup redis-server /etc/redis/redis.conf &
<<<<<<< HEAD
#gunicorn hemera:app -k gevent -b 0.0.0.0:5000
gunicorn hemera:app -k gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" -b 0.0.0.0:5000
=======
/usr/local/python279/bin/gunicorn hemera:app -k gevent -b 0.0.0.0:5000
>>>>>>> abc7ef6a675f31069258215b6d3fd65927c7e45a
#nohup gunicorn -b 0.0.0.0:80 -k eventlet -w 40 -t 99999 run:app &

#hello world
