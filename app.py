from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  #либо я ввожу сама, либо оно вводится став авт.

@app.route("/")
@app.route("/main")
def main_page():
    return render_template('start_page.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/user/<string:name>/<int:id>")
def user(name, id):
    return f"User page: {name}, {id}"


@app.route("/try")
def my_try():
    return render_template('index.html')


@app.route("/create", methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form["title1"]
        intro = request.form["intro1"]
        text = request.form["text1"]

        post = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect("read_posts")
        except:
            raise "Ошибка"

    return render_template('create.html')


@app.route("/<int:id>/update", methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form["title1"]
        article.intro = request.form["intro1"]
        article.text = request.form["text1"]
        try:
            db.session.commit()
            return redirect("/read_posts")
        except:
            raise "Ошибка"
    return render_template('update_article.html', article=article)

@app.route("/read_posts")
def read_posts():
    shakalaka = Article.query.order_by('date').all()[::-1]
    return render_template('read_posts.html', myp=shakalaka)

@app.route("/<int:id>")
def more(id):
    full_read = Article.query.filter_by(id=id)
    return render_template('more.html', full_read=full_read)

@app.route("/<int:id>/del")
def del_post(id):
    del_param = Article.query.get(id)
    try:
        db.session.delete(del_param)
        db.session.commit()
        return redirect("/read_posts")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Ошибка {e}")
        return "При удвлении проитзошла ошибка"







if __name__ == "__main__":
    app.run(debug=True)
