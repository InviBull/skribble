from flask import Blueprint, redirect, request
from flask_login import login_required, login_user, logout_user 
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from db.models import User

from utils.env import env
from db.db import mutate, query

auth = Blueprint('auth', __name__, template_folder='templates')
client = WebApplicationClient(env("GOOGLE_CLIENT_ID"))

def get_google_provider_cfg():
    return requests.get("https://accounts.google.com/.well-known/openid-configuration").json()

@auth.route('/auth/login')
def login():
    cfg = get_google_provider_cfg()
    authorization_endpoint = cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri = request.base_url + '/callback',
        scope = ["openid", "email", "profile"]
    )

    return redirect(request_uri)

@auth.route('/auth/login/callback')
def googleCallback():
    code = request.args.get("code")
    cfg = get_google_provider_cfg()
    token_endpoint = cfg['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers = headers,
        data = body,
        auth=(env("GOOGLE_CLIENT_ID"),env("GOOGLE_CLIENT_SECRET") )
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    user = userinfo_response.json()
     
    if user.get("email_verified"):
        id = user['sub']
        email = user['email']
        avatar = user['picture']
        name = user['given_name']
    else:
        return "Email not verified", 400

    user = query("SELECT id FROM users where id = ?", (id,))
    if len(user) == 0:
        mutate("INSERT INTO users (id, name, email, avatar) values (?, ?, ?, ?)", (id, name, email, avatar,))
        user = query("SELECT id FROM users where id = ?", (id,))

    login_user(User(user[0][0]))
    return redirect('/')

@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
