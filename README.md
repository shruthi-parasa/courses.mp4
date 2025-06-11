# Courses.MP4

To run the app locally, add a .env file with `PORT=8000`, your YouTube API Key with `YOUTUBE_API={your API key}`, 
and `MONGO_URI=mongodb://root:rootpassword@localhost:27017/mydatabase?authSource=admin`

The Youtube API key can be sourced from the Google Developer Console - Youtube V3 Data API

Run the app on the prod environment; once docker is running, insert the sample data into MongoDB by running the temp_fetching.py script located in the backend directory with a venv that has the requirements installed.
(Note that you could use fetch.py, which fetches and processes all data and puts it all into MongoDB, however due to the limitations of the Youtube V3 Data API, we cannot extract all the videos of our course collection at once)
