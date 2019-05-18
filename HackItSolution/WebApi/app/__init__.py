from flask import Flask, render_template
from app.mod_api.controllers import mod_api as api_module


app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(api_module)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('public/index.html')
