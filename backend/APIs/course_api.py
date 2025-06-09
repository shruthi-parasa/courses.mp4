from bs4 import BeautifulSoup
import requests
import re

def extractCoursesProtocol(req_url):
    response = requests.get(req_url)
    # BeautifulSoup function, link here https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    soup = BeautifulSoup(response.content, 'html.parser')
   
    # Extract each courseblock <div>, see the html provided by the General Catalog Network Tab for more detail
    course_blocks = soup.find_all('div', class_='courseblock')
   
    courses = []
    for block in course_blocks:
        # Allows us to extract info from each course cleanly, at this point we only have the block as a whole
        courseData = getCourseInfo(block)
        # Filter out courses with numbers >= 200 or invalid courses
        if courseData and noGrads(courseData.get('code', '')):
            courses.append(courseData)
   
    return courses

def noGrads(course_code):

    if not course_code:
        return False
    
    # Regex to catch anything starting with 2 or 3
    pattern = r'(2|3)\d\d[a-z]?'
    
    if re.search(pattern, course_code.lower()):
        return False
    
    return True

def getCourseInfo(course_block):
    # Dict necessary for pair values for each course
    course_info = {}
   
    # Must traverse the courseblock each time, see the html provided by the General Catalog Network Tab for more detail :)
    header = course_block.find('h3', class_='cols noindent')
    # Each course will have own sub array of info, can add more info such as Units and Prerequisites if necessary
    if header:
        code_span = header.find('span', class_='detail-code')
        if code_span:
            course_info['code'] = code_span.get_text().strip().replace(" ", "").lower()
       
        title_span = header.find('span', class_='detail-title')
        if title_span:
            course_info['title'] = title_span.get_text().replace('—', '').strip()
   
    # This is located outside of the header div, must extract outside of the header search
    desc_p = course_block.find('p', class_='courseblockextra')
    if desc_p:
        desc_text = desc_p.get_text()
        if 'Course Description:' in desc_text:
            course_info['description'] = desc_text.split('Course Description:')[1].strip()
        else:
            course_info['description'] = desc_text.strip()
   
    return course_info
 
def fetchCoursesByCode(course_code):
    course_code = course_code.lower()
    request_url = f"https://catalog.ucdavis.edu/courses-subject-code/{course_code}/"
    courses = extractCoursesProtocol(request_url)
    return courses

if __name__ == "__main__":
    # Test the function
    courses = fetchCoursesByCode("ecs")
    for course in courses:
        print(f"Course Code: {course['code']} - Course Title: {course['title']}")