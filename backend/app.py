from flask import Flask, redirect, url_for, session, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
import json
from pymongo import MongoClient
from flask_cors import CORS

static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo["database"]

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = os.urandom(24)

oauth = OAuth(app)

nonce = generate_token()



oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    #server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

flask_app = oauth.create_client(os.getenv('OIDC_CLIENT_NAME'))


@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Get a list of all course codes in our system
@app.route('/api/courses_list', methods=["GET"])
def get_courses_list():
  curr_dir = os.path.dirname(os.path.abspath(__file__))
  courses_path = os.path.join(curr_dir, 'data', 'course_list.json')
  
  with open(courses_path, "r") as file:
    courses = json.load(file)
  
  return courses
  
# Get videos for a course code
@app.route('/api/videos/<course_code>', methods=["GET"])
def get_videos(course_code):
  entry = db["videos"].find_one({"code": course_code})
  videos = entry["videos"]
  return jsonify(videos)

# Get course information for a course code
@app.route('/api/courses/<course_code>', methods=["GET"])
def get_course_info(course_code):
  course = db["course-info"].find_one({"code": course_code})
  return jsonify({
    "title": course["title"],
    "description": course["description"]
  })

# Get test course data
@app.route('/api/test_courses', methods=["GET"])
def get_test_courses():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    courses_path = os.path.join(curr_dir, 'data', 'test_course_info.json')
    
    with open(courses_path, "r") as file:
        courses = json.load(file)
    
    return jsonify(courses)

@app.route('/get-user')
def get_user():
    # gets the logged in user's username from the db
    # @returns the username in JSON
    user = session.get('user')
    if (not user):
        return jsonify({'username': None})
    return jsonify({'username': f"{user['name']}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    # app.run(debug=True, host='0.0.0.0', port=8001)
