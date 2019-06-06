from app import app, db
from app.models import User, Account

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Account': Account}

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

# sudo pip3 install flask
# sudo pip3 install flask-wtf 
# sudo pip3 install flask-sqlalchemy
# sudo pip3 install flask-migrate
# sudo pip3 install flask-login
# sudo pip3 install Flask-Boostrap

# flask db init
# flask db migrate -m "users movements accounts table"
# flask db upgrade

# Cuando hayamos agregado todos los usuarios, toca editar los valores 

# Crear tres usuarios, dos que intercambian entre si y el usuario atacante.

# syper - 53Cre71234@! ==> 16000
# pepito - qwerty1234 ==> 100
# user17 - asd123 ==> 0

# update account SET amount = <amount> where username = '<name>';
# update account SET amount = 16000 where username = 'syper';
# update account SET amount = 100 where username = 'pepito';

# update account SET amount = 0 where username = 'user17';
