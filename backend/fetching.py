# Fetch courses and video
# Would store into database later. Using json files for now

import json
import os
from pymongo import MongoClient

from courseAPI.course_api import fetchCoursesByCode
from extract_keywords.extract_keywords import extract_keywords
from youtube.youtube import fetch_videos

mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo["database"]

# Fetch courses using department codes
# Extract keywords for courses
def process_courses():
  curr_dir = os.path.dirname(os.path.abspath(__file__))
  file_course_info = os.path.join(curr_dir, 'data', 'test_course_info.json')
  file_course_list = os.path.join(curr_dir, 'data', 'course_list.json')
  
  courses = dict()
  course_list = []
  
  courses_codes = ["ecs"]
  
  for code in courses_codes:
    course_info = fetchCoursesByCode(code)
    # course_info = [
    #   {
    #     "code": "ecs036c",
    #     "title": "Data Structures, Algorithms, & Programming",
    #     "description": "Design and analysis of data structures for a variety of applications; trees, heaps, searching, sorting, hashing, and graphs. Extensive programming."
    #   },
    #   {
    #     "code": "ecs150",
    #     "title": "Operating Systems & System Programming",
    #     "description": "Basic concepts of operating systems and system programming. Processes and interprocess communication/synchronization; virtual memory, program loading and linking; file and I/O subsystems; utility programs. Study of a real operating system."
    #   },
    #   {
    #     "code": "ecs162",
    #     "title": "Web Programming",
    #     "description": "Technical aspects of building websites, including both server-side and client-side software development."
    #   }
    # ]
    
    for course in course_info:
      course_list.append(course["code"])
      print(course["code"])
      keyword = extract_keywords(course["title"] + ": " + course["description"])
      courses[course["code"]] = {
        "title": course["title"],
        "description": course["description"],
        "keywords": keyword
      }
      
      db["course-info"].insert_one({
        "code": course["code"],
        "title": course["title"],
        "description": course["description"],
        "keywords": keyword
      })
  
  with open(file_course_info, "w") as file:
    json.dump(courses, file, indent=2)
    
  with open(file_course_list, "w") as file:
    json.dump(course_list, file, indent=2)
    
# Get videos for all keywords
def get_videos():
  curr_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(curr_dir, 'data', 'test_course_info.json')
  
  with open(file_path, "r") as file:
    courses = json.load(file)
  
  for code, course_info in courses.items():
    keywords = course_info["keywords"]
    
    videos = []
    for keyword in keywords:
      videos.extend(fetch_videos(keyword, 3))
      
    course_info["videos"] = videos
    
    db["videos"].insert_one({
      "code": code,
      "videos": videos
    })
    
  with open(file_path, "w") as file:
    json.dump(courses, file, indent=2)
  

if __name__ == "__main__":
  process_courses()
  get_videos()
  