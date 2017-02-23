# all the imports
import time
import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#from flask_bootstrap import Bootstrap
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

#from .admin.views import adm
#app.register_blueprint(adm, url_prefix='/admin')
from .console.views import cns
app.register_blueprint(cns, url_prefix='/console')
from .launcher.views import lau
app.register_blueprint(lau, url_prefix='/launcher')
#from .launcher.views import sse
#app.register_blueprint(sse, url_prefix='/stream')

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

#################################  Decorator  #################################

def timeformat(timestamp, format='%Y%m%d-%H:%M:%S'):
    timeArray = time.localtime(timestamp)
    return time.strftime(format, timeArray)

app.jinja_env.filters['timeformat'] = timeformat

















#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
##app.config.from_pyfile(os.environ.get('FLASKR_SETTINGS'))
##app.config.from_pyfile('config.cfg') ##ok
##app.config.from_pyfile('/search/odin/flasky/flaskr/config.cfg') ##ok
##app.config.from_object(__name__)
##app.config.from_object('yourapplication.default_config')
##from yourapplication import default_config
##app.config.from_object('config.cfg')
##app.config['DATABASE'] = '/tmp/flaskr.db'
##app.config['USERNAME'] = 'duyichen'
##app.config['PASSWORD'] = 'dudu'
##app.config['SECRET_KEY'] = 'hard to guess string'
##app.config['DEBUG'] = True
#################################################################################################
#
#def connect_db():
#    """Connects to the specific database."""
#    rv = sqlite3.connect(app.config['DATABASE'])
#    #rv.row_factory = sqlite3.Row
#    return rv
#
#def init_db():
#    #with app.app_context():
#    #    db = get_db()
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql', mode='r') as f:
#            db.cursor().executescript(f.read())
#        db.commit()
#
#def get_db():
#    """Opens a new database connection if there is none yet for the
#    current application context.
#    """
#    if not hasattr(g, 'sqlite_db'):
#        g.sqlite_db = connect_db()
#    return g.sqlite_db
#
#################################################################################################
#
#@app.before_request
#def before_request():
#    g.db = connect_db()
#
#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(g, 'db', None)
#    if db is not None:
#        db.close()
#
##@app.teardown_appcontext
##def close_db(error):
##    """Closes the database again at the end of the request."""
##    if hasattr(g, 'sqlite_db'):
##        g.sqlite_db.close()
#
#@app.route('/')
#def show_entries():
#    cur = g.db.execute('select title, text from entries order by id desc')
#    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
#    entries = 'hello'
#    return render_template('show_entries.html', entries=entries)
#
#@app.route('/add', methods=['POST', 'GET'])
#def add_entry():
#    if not session.get('logged_in'):
#        abort(401)
#    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
#    g.db.commit()
#    flash('New entry was successfully posted')
#    return redirect(url_for('show_entries'))
#
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    error = None
#    if request.method == 'POST':
#        if request.form['username'] != app.config['USERNAME']:
#            error = 'Invalid username'
#        elif request.form['password'] != app.config['PASSWORD']:
#            error = 'Invalid password'
#        else:
#            session['logged_in'] = True
#            flash('You were logged in')
#            return redirect(url_for('show_entries'))
#    return render_template('login.html', error=error)
#
#@app.route('/logout')
#def logout():
#    session.pop('logged_in', None)
#    flash('You were logged out')
#    return redirect(url_for('show_entries'))
#
##class rend_template(View):
##    def __init__(self,t_name):
##        self.tmp_name = t_name
##    def dispatch_request(self):
##        return render_template(self.tmp_name)
##
#app.add_url_rule('/about',view_func=rend_template.as_view('about_page', t_name='about.html'))
#
#
#################################################################################################
#if __name__ == '__main__':
#    app.run('0.0.0.0')
