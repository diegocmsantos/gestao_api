# all the imports
import sqlite3, sys
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = '/home/diego/gestao/db/gestao.db'
DEBUG = False
SECRET_KEY = 'qwe123*'
USERNAME = 'admin'
PASSWORD = '123456'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
		
@app.route('/')
def show_usuarios():
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    #return render_template('show_entries.html', entries=entries)
    return 'Teste'

@app.route('/logacesso', methods=['POST'])
def add_log_acesso():
    #if not session.get('logged_in'):
        #abort(401)
    try:
        g.db.execute('INSERT INTO importacao (usuario_id, tipo_importacao, dataImportacao) values (?, ?, ?)',
            [request.form['usuario_id'], request.form['tipo_importacao'], request.form['data_importacao']])
        g.db.commit()
    except:
        print "Erro inesperado", sys.exc_info()
        return "Erro", 500
    return '200', 201

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    if not session.get('logged_in'):
        abort(401)
    try:
        g.db.execute('insert into usuario (usuario, senha, dataAcesso, cnpj) values (?, ?, ?, ?)',
            [request.form['usuario'], request.form['senha'], request.form['dataAcesso'], request.form['cnpj']])
        g.db.commit()
    except:
        print "Erro inesperado:", sys.exc_info()
        return 'Erro', 500
    return '200', 201

@app.route('/autenticar', methods=['GET'])
def autenticar():
    c = g.db.cursor()
    c.execute("select * from usuario where usuario = ? and senha = ?",
                 [request.args['usuario'], request.args['senha']])
    if c.fetchone():
        session['logged_in'] = True
        return 'ok', 200
    else:
        return 'nok', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0')
