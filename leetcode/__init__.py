from flask import Flask, render_template, request, abort, session, redirect
# All other modules depend on app, so it shall created before other modules imported.
app = Flask(__name__)

from .config import local_config
import json
import os
from .logger import init_logger
from .server.center import Center

center = Center()
init_logger(app)
app.config['SECRET_KEY'] = "leetcode!Dasdq912QW%$F@#$TG$%%12323f4"

@app.route('/')
def index():
    return redirect('/ranklist/1/', code = 302)

@app.route('/ranklist/<int:page>/')
def ranklist(page):
    p = center.get_rank_page(page)
    return render_template('rank_list.html',
            page = page,
            max_page = (p.total_users + p.user_per_page - 1) // p.user_per_page,
            users = p.users
        )

@app.route('/u/<user_name>/')
def user(user_name):
    u = center.get_user(user_name)
    if u == None:
        abort(404)
    return render_template('user.html',
            user = u
        )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 


