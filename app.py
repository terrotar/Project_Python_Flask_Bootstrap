from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Cada id será único, como criado no DBeaver
    # Note também q o "id" foi definido a chave primaria
    title = db.Column(db.String(100), nullable=False)
    # Aqui foi delimitado o número máx de caracteres e
    # também foi definido o NOT NULL em criação de tabelas
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    # Default é o padrão caso a coluna esteja vazia
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return f"Blog post {self.id}"
    # o __repr__ dá um print qndo se cria a classe


@app.route('/')
def index():
    return render_template('index.html')


# Route dos posts
@app.route('/posts', methods=['GET'])
def posts():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)


# Route do new_post
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if (request.method == 'POST'):
        posts_title = request.form['title']
        posts_content = request.form['content']
        posts_author = request.form['author']
        new_post = BlogPost(title=posts_title,
                            content=posts_content, author=posts_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


# Route do delete
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# Route do edit
# Repare q os 'methods' foram definidos pois irá enviar
# um valor e receber também, diferente do 'delete'
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if (request.method == 'POST'):
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


# Route de exemplo de variável
@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return f"Hello, {name} ! Your id is: {id}."


# Route de exemplo de 'GET' e 'POST'
@app.route('/onlyget', methods=['GET'])
def get_req():
    return "You can only get this webpage. 4"


if __name__ == "__main__":
    app.run(debug=True)
