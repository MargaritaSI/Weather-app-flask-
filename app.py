from flask import Flask, render_template, url_for, request, redirect #rt - connects flask + html, url_for - for tamplates
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/margaritasmyslava/PycharmProjects/Weather/blog.db'

db = SQLAlchemy()
db.init_app(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), primary_key=False)
    intro = db.Column(db.String(300), primary_key=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id #object + id object from db


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles) # pass to template list 'articles'(2) and in template we could have acsess to this list with key word 'articles'(1) and work in template

@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article) #

@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except: 'error during deleting posts'

@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error during update topic"
    else:
        return render_template('post_update.html', article=article)

@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error during adding topic"
    else:
        return render_template('create-article.html')


if __name__=='__main__':
    app.run(debug=True)
