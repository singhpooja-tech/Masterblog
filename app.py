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


@app.route('/')
def index():
    """Rendering the index template
    Homepage"""
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


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


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update function for a post"""

    # Fetch the blog posts from the JSON file
    blog_posts = load_posts()

    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        post['author'] = request.form.get('author', post['author'])
        post['title'] = request.form.get('title', post['title'])
        post['content'] = request.form.get('content', post['content'])

        save_posts(blog_posts)

        # Redirect back to index
        return redirect(url_for('index'))

        # Else, it's a GET request
        # So display the update.html page

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """Like button for posts"""
    # Fetch the blog posts from the JSON file
    blog_posts = load_posts()

    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        # post not found
        return "Post not found", 404

    # Updating likes
    post['likes'] += 1

    save_posts(blog_posts)

    # Redirect back to the index page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
