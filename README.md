# Courses.MP4

To run the app locally, add a .env file with `PORT=8000`, your YouTube API Key with `YOUTUBE_API={your API key}`, 
and `MONGO_URI=mongodb://root:rootpassword@localhost:27017/mydatabase?authSource=admin`

The Youtube API key can be sourced from the Google Developer Console - Youtube V3 Data API

Run the app on the prod environment; once docker is running, insert the sample data by running the temp_fetching.py
script located in the backend directory with a venv that has the requirements installed.