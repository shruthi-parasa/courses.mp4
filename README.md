# Courses.MP4  

A web application that recommends YouTube videos based on university courses. Students can input their classes and receive curated video content tailored to their learning needs.  

## Tech Stack  
- **Frontend:** Svelte, JavaScript, HTML/CSS  
- **Backend:** Flask (Python), MongoDB  
- **APIs:** YouTube V3 Data API  
- **Other:** Docker, Node.js, PyTest  

## My Contributions  
- Built and tested the **Svelte frontend** for displaying YouTube videos in a responsive 3-column grid  
- Integrated YouTube API results with backend data to provide course-based recommendations  
- Collaborated in a 4-person team to design and document full-stack functionality  

## Getting Started  

To run the app locally, add a .env file with `PORT=8000`, your YouTube API Key with `YOUTUBE_API={your API key}`, 
and `MONGO_URI=mongodb://root:rootpassword@localhost:27017/mydatabase?authSource=admin`

- The YouTube API key can be sourced from the Google Developer Console (YouTube Data API v3).  

### Running the App  
1. Start Docker  
2. Insert sample data into MongoDB by running `temp_fetching.py` in the backend directory with a virtual environment containing the required dependencies.  
   - *(Optional)* Use `fetch.py` to fetch and process all data, though note the API’s video extraction limits.  

### Running Tests  
- **Frontend tests:**  
cd frontend/frontend_tests
npm install
sudo npm test

- **Backend tests:**  
cd backend/tests
pytest

---
