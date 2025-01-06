from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    """Loading the json file"""
    try:
        with open('blog_posts.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Saving to json file"""
    with open('blog_posts.json', 'w', encoding='utf-8') as file:
        return json.dump(posts, file, indent=4)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add option for a post
    User can choose author, title
    and the content"""
    if request.method == 'POST':
        blog_posts = load_posts()

        id_gen = max((post['id'] for post in blog_posts), default=0) + 1
        new_post = {
            'id': id_gen,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'likes': 0
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Adding delete option for a post"""
    blog_posts = load_posts()

    # Find the blog post with the given id and remove it from the list
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_posts(blog_posts)
    # Redirect back to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)