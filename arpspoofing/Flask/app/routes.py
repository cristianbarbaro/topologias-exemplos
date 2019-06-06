from flask import render_template, flash, redirect, request, url_for, abort
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Account, Movement
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import MovementForm
import hashlib


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Inicio', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o contraseñas inválidas.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Iniciar sesión', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        account_number = str(int(hashlib.md5((username).encode("utf-8")).hexdigest(), 24))[:16]
        #account_number = int(hashlib.md5((username).encode("utf-8")).hexdigest()[:16], 18)
        account = Account(amount=0, number=account_number)

        user = User(username=username, email=form.email.data, accounts=[account])
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Usted ha sido registrado correctamente.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrar', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    account = Account.query.filter_by(user_id=user.id).first_or_404()

    return render_template('user.html', user=user, account=account)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Sus cambios han sido guardados.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Editar usuario',
                           form=form)


@app.route("/transaction", methods=["GET", "POST"])
@login_required
def create_transaction():
    form = MovementForm()
    if form.validate_on_submit():
        # Debemos restarle plata al usuario logueado y darsela al otro usuario (que debe existir)
        transaction_amount = form.amount.data 
        transaction = Movement(receiver=form.receiver.data,reason=form.reason.data,amount=transaction_amount)        
        
        current = User.query.filter_by(id=current_user.id).first_or_404()

        receiver_account = Account.query.filter_by(number=str(form.receiver.data)).first_or_404()

        current_account = current.accounts[0]

        # Si nuestro cliente tiene dinero para transferir, se lleva a cabo dicha transferencia
        if current_account.amount >= transaction_amount:
            current_account.amount = float(current_account.amount) - float(transaction_amount)
            receiver_account.amount = float(receiver_account.amount) + float(transaction_amount)
        else:
            flash ("No cuenta con suficiente dinero para realizar la transacción. Intente nuevamente con un valor diferente.")
            return redirect(url_for("create_transaction"))

        current.transactions.append(transaction)
        db.session.commit()
        flash('Transacción realizada correctamente.')
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.amount.data = 0
        form.receiver.data = 0
    return render_template("create_transaction.html", title="Transacción", form=form)


@app.route("/user/transactions/<user_id>")
@login_required
def transactions(user_id):
    if int(user_id) == current_user.id:
        user = User.query.filter_by(id=user_id).first_or_404()
        transactions = user.transactions
        return render_template("transactions.html", tittle="Transacciones usuario", transactions=transactions)
    else:
        abort(403)

