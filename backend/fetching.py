# Fetch courses and video
# Would store into database later. Using json files for now

import json
import os

from courseAPI.course_api import fetchCoursesByCode
from extract_keywords.extract_keywords import extract_keywords
from youtube.youtube import fetch_videos

# Fetch courses using department codes
# Extract keywords for courses
def process_courses():
  curr_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(curr_dir, 'data', 'course_info.json')
  
  courses = dict()
  
  courses_codes = ["ecs", "eec"]
  
  for code in courses_codes:
    course_info = fetchCoursesByCode(code)
    
    for course in course_info:
      courses[course["code"]] = {
        "title": course["title"],
        "description": course["description"],
        "keywords": extract_keywords(course["title"] + ": " + course["description"])
      }
  
  with open(file_path, "w") as file:
    json.dump(courses, file, indent=2)
    
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
    
  with open(file_path, "w") as file:
    json.dump(courses, file, indent=2)
  

if __name__ == "__main__":
  process_courses()
  get_videos()
  