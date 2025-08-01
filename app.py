from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import RegisterForm, LoginForm
from models import User, init_db
from forms import EditProfileForm


app = Flask(__name__) 
app.config['SECRET_KEY'] = 'your-secret-key'

init_db()  # Created DB & table on startup

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


users = {'testuser': User(id=1, username='testuser', password='pass123')}

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.get_by_username(form.username.data)
        if existing_user:
            flash('Username already exists. Try another.', 'error')
            return redirect(url_for('register'))
        User.create(form.username.data, form.password.data)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile') 
@login_required
def profile():
    friends = User.get_connections(current_user.id)
    return render_template('profile.html', name=current_user.username, friends=friends)

@app.route('/users')
@login_required 
def users():
    other_users = User.get_all_except(current_user.id)
    return render_template('user_directory.html', users=other_users, current_user=current_user, is_connected=User.is_connected)

@app.route('/connect/<int:user_id>', methods=['POST']) 
@login_required
def connect(user_id):
    User.add_connection(current_user.id, user_id)
    return redirect(url_for('users'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.update_profile(form.age.data, form.bio.data, form.interests.data)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)
        
@app.route('/user/<int:user_id>')
@login_required
def view_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        return render_template('view_user.html', user=user)
    else:
        flash("User not found.", "error")
        return redirect(url_for('users'))
    
    # Pre-fill with current data
    form.age.data = current_user.age
    form.bio.data = current_user.bio
    form.interests.data = current_user.interests
    return render_template('edit_profile.html', form=form)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)



