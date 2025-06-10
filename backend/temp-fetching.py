import os
import json
from pymongo import MongoClient

mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo["database"]

curr_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(curr_dir, 'data', 'course_info.json')

with open(file_path, "r") as file:
  courses = json.load(file)

for code, course_info in courses.items():
  db["course-info"].insert_one({
    "code": code,
    "title": course_info["title"],
    "description": course_info["description"],
    "keywords": course_info["keywords"]
  })
  
  db["videos"].insert_one({
    "code": code,
    "videos": course_info["videos"]
  })
  
db["user-courses"].insert_one({
  "username": "user@hw3.com",
  "courses": [
    "ecs162"
  ]
})

db["user-courses"].insert_one({
  "username": "moderator@hw3.com",
  "courses": [
    "ecs162"
  ]
})

db["user-courses"].insert_one({
  "username": "admin@hw3.com",
  "courses": [
    "ecs162"
  ]
})