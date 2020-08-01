from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path as path

app = Flask(__name__)
app.secret_key = "anddasnasndnasn"

@app.route('/')
def index():
    return render_template('index.html', title="URL Shortner", codes=session.keys())

@app.route('/about')
def about():
    return "<h1>This is Url shortner</h1>"

@app.route('/your-url', methods=['GET', 'POST'] )
def your_url():
    if request.method == 'POST':
        urls = {}

        if path.exists('url.json'):
            with open('url.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash("This ShortNAme is Already Taken")
            return redirect(url_for('index'))

        urls[request.form['code']] = {'url': request.form['url']}
        with open('url.json', 'w') as url_json:
            json.dump(urls,url_json)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('index'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if path.exists('url.json'):
        with open('url.json') as urls_file:
            urls = json.load(urls_file)
        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
    return abort(404)


@app.errorhandler(404)
def error_handler(error):
    return render_template('404.html')


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


