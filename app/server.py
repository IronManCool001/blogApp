from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Anonmyous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)
X = ['Hello','Bye']
@app.route('/')
def home():
    name = request.cookies.get('name')
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    logged=request.cookies.get('logged')
    return render_template('index.html', len=len(X), posts = all_posts, name=name)
@app.route('/login')
def login():
    logged=request.cookies.get('logged')
    if logged == "true":
        return render_template('login.html', logged=True)
    else:
        return render_template('login.html', logged=False)
@app.route('/createPost')
def createPost():
    name = request.cookies.get('name')
    if name == "null":
        null = True
        return render_template('posts.html', null=null)
    else:
        return render_template('posts.html')

@app.route('/dashboard')
def dashboard():
    name = request.cookies.get('name')
    email = request.cookies.get('Email')
    imageURL= request.cookies.get('imageURL')
    return render_template('dashboard.html',name=name,email=email,imgurl=imageURL)
@app.route('/posts', methods=['POST','GET'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        name = request.cookies.get('name')
        if post_author != name:
            error = True
            return render_template('posts.html',error=True)
        else:
            new_post = BlogPost(title=post_title, content=post_content, author=post_author)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
    else:
        return redirect('/')

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(debug=True)
