
from flask import render_template, flash, redirect,session, url_for,request, g
from flask_login import login_user, logout_user, current_user,login_required

from app import app, db, lm, oid
from app.forms import LoginForm, UserEditForm,PostForm
from app.models import User, Post, ROLE_USER,ROLE_ADMIN
from datetime import datetime

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.now()
		db.session.add(g.user)
		db.session.commit()

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login, Pls try again.')
		redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))	

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
	#print("helloworld...")
	user = g.user # fake user'
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body = form.post.data, timestamp = datetime.now(), author = user)
		db.session.add(post)
		db.session.commit()
		flash('your post is now live!')
		return redirect(url_for('index'))

	#posts = [
	#	{
	#		'author': {'nickname': 'John'},
	#		'body': 'Beautiful day in Portland!'
	#	},
	#	{
	#		'author': {'nickname': 'Susan'},
	#		'body': 'The Avengers movie was so cool!'
	#	}
	#]
	posts = user.followed_posts().all()
	app.logger.info('posts size %s' %(posts))
	print('posts size %s' %(posts))
	return render_template('index.html',title='Home', form = form, user = user, posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	#print("11111111111111")
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	#print("data:%s" %(form.openid.data))	
	
	if form.validate_on_submit():
		#flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		#return redirect('/index')
		#print("33333333333")
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	#print("4444444444444")	
	return render_template('login.html', title='登录', form = form, providers = app.config['OPENID_PROVIDERS'])	

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('不存在用户:%s！' %(nickname) )
		return redirect(url_for('index'))
	posts = [
		{ 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
	]
	return render_template('user.html',user = user, posts = posts)


@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = UserEditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form = form)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404
 
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500