from flask import Flask,request,redirect,render_template,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(20), nullable=False, default='Anonmyous')

    def __repr__(self):
        return 'User ' + str(self.id)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Anonmyous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

@app.route('/')
def home():
    name = request.cookies.get('name')
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    logged = bool(name)
    return render_template('index.html', posts = all_posts, name=name,logged=logged)
@app.route('/login')
def login():
    name = request.cookies.get('name')
    logged = bool(name)
    if logged:
        return redirect('/')
    else:
        return render_template('login.html',pserror=False,nerror=False,logged=logged)

@app.route('/register')
def signup():
    name = request.cookies.get('name')
    logged = bool(name)
    if logged:
        return redirect('/')
    else:
        return render_template('signup.html',error=False,logged=logged)

@app.route('/dashboard')
def dashboard():
    name = request.cookies.get('name')
    logged = bool(name)
    if logged:
        user = User.query.filter_by(name=name).first()
        email = user.email
        return render_template('dashboard.html',logged=logged,name=name,email=email)
    else:
        return render_template('dashboard.html',logged=False)

@app.route('/createpost')
def createPost():
    name = request.cookies.get('name')
    if (bool(name) == False):
        null = True
        logged = False
        return render_template('posts.html', null=null,logged=logged)
    else:
        logged = True
        return render_template('posts.html',logged=logged)
@app.route('/about')
def about():
    name = request.cookies.get('name')
    logged = bool(name)
    return render_template('about.html',logged=logged)

@app.route('/post/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    name = request.cookies.get('name')
    if name == post.author:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        name = request.cookies.get('name')
        post.title = request.form['title']
        #post.author = name
        post.content = request.form['content']
        if post.author == name:
            post.author = name
            db.session.commit()
            return redirect('/post')
        elif(post.author != name):
            return redirect('/')
    else:
        return render_template('edit.html', post=post)

@app.route('/post', methods=['POST','GET'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        name = request.cookies.get('name')
        new_post = BlogPost(title=post_title, content=post_content, author=name)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/checkaccount',methods=['POST','GET'])
def checkaccount():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if bool(user):
            if (user.name == name):
                if (user.password == password):
                    if (bool(name) == True):
                        response = make_response( redirect('/') )
                        response.set_cookie( "name", name)
                        return response
                    else:
                        return redirect('/login')
                if (user.password != password):
                    return render_template('login.html',pserror=True)
            else:
                return render_template('login.html',nerror = True)
        else:
            return redirect('/register')

@app.route('/newaccount',methods=['POST','GET'])
def newaccount():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existingname = User.query.filter_by(name=name).first()
        if (bool(existingname)):
            return render_template('signup.html',error=True)
        else:
            if (bool(name) == True):
                newaccount = User(name=name, email=email, password=password)
                db.session.add(newaccount)
                db.session.commit()
                return redirect('/login')
            else:
                return redirect('/register')

if __name__ == "__main__":
    app.run(debug=True)
