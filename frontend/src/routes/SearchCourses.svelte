<script lang="ts">
  import {getUser} from '../get_user';
  // Search for Courses page logic will go here
  
  interface Video {
    title: string;
    id: string;
    channel: string;
    thumbnail: string;
    video_url: string;
    up_vote: number;
    down_vote: number;
  }

  interface Course {
    code: string;
    title: string;
    description: string;
    keywords: string[];
    videos: Video[];
  }
  let courses: Course[] = [];
  let loading = true;
  let error: string | null = null;
  let searchPhrase = '';
  let favoriteCourses = new Set<string>();
  let showCourseViewer: boolean = false;
  let courseInViewer: Course | null = null;
  let selectedVideo: Video | null = null;  let userCourses: any[] = [];
  let allCourses: any[] = [];
  let filteredCourses: any[] = [];
  let isLoggedIn = false;

  // User vote tracking
  let userVotes: { upvote: string[], downvote: string[] } = { upvote: [], downvote: [] };

  $: availableCourses = allCourses.filter(course => !userCourses.includes(course.code));

  // Update your filtering logic to use availableCourses instead of courses
  $: filteredCourses = availableCourses.filter(course => 
    course.code.toLowerCase().includes(searchPhrase.toLowerCase()) ||
    course.title.toLowerCase().includes(searchPhrase.toLowerCase()) ||
    course.description.toLowerCase().includes(searchPhrase.toLowerCase()) ||
    course.keywords.some((keyword: string) => keyword.toLowerCase().includes(searchPhrase.toLowerCase()))
  );

  
  //Need to check the available coures against the user's current favorite and added courses
  //Only show class that aren't already a part of the user's storage
  import { onMount } from 'svelte';  onMount(async () => {
    let username = await getUser();
    isLoggedIn = !!username;
    await fetchUserCourses();
    fetchCourses();
    if (isLoggedIn) {
      await getUserVotes();
    }
  });


  function triggerFavs(code: string) {
    if (favoriteCourses.has(code)) {
      favoriteCourses.delete(code);
    } else {
      favoriteCourses.add(code);
    }
    favoriteCourses = favoriteCourses;
    // Save to localStorage
    localStorage.setItem('favoriteCourses', JSON.stringify(Array.from(favoriteCourses)));
  }

  async function fetchUserCourses(){
    try{
      const res = await fetch ('/api/user/courses');
      const data = await res.json();
      userCourses = data;
    } catch(e){
      console.log("Error occured: ", e);
    }
  }

  async function fetchCourses() {
    try {
      // Fetch test course data
      const response = await fetch('/api/test_courses');
      if (!response.ok) throw new Error('Failed to fetch courses');
      const courseData = await response.json();
      
      // Transform the data into our Course interface format
      allCourses = Object.entries(courseData).map(([code, data]: [string, any]) => ({
        code,
        title: data.title,
        description: data.description,
        keywords: data.keywords,
        videos: data.videos
      }));
      console.log("All Courses - ", allCourses);
      console.log("User Courses - ", userCourses);
      courses = allCourses.filter(course => !userCourses.includes(course.code));
      console.log("Filtered Courses - ", courses);
      loading = false;
    } catch (e) {
      error = e instanceof Error ? e.message : 'An error occurred';
      loading = false;
    }
  }

  // Load favorites from localStorage
  function loadFavorites() {
    const favs = localStorage.getItem('favoriteCourses');
    if (favs) {
      try {
        favoriteCourses = new Set(JSON.parse(favs));
      } catch {}
    }
  }

  async function addCourse(courseInfo: any){
    if (!isLoggedIn) {
      alert('Please log in to add courses to your account.');
      return;
    }
    let courseCode = courseInfo;
    console.log("Course to Add - ", courseCode.code);
    try {
      const response = await fetch('/api/user/courses/add', {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          course: courseCode.code
        })
      });
      
      const result = await response.json();

      if(response.ok){
        console.log("You've successfully added a course!");
        await fetchUserCourses();
      }
      
    } catch (err) {
      console.error('Error adding course:', err);
    }
  }

  // Load favorites when component mounts
  loadFavorites();

  // Filtering courses based on search phrase
  // *****Updated reactive statements near the top by the variables declarations*****
  // $: filteredCourses = courses.filter(course => 
  //   course.code.toLowerCase().includes(searchPhrase.toLowerCase()) ||
  //   course.title.toLowerCase().includes(searchPhrase.toLowerCase()) ||
  //   course.description.toLowerCase().includes(searchPhrase.toLowerCase()) ||
  //   course.keywords.some(keyword => keyword.toLowerCase().includes(searchPhrase.toLowerCase()))
  // );

  function showCourseDetails(course: Course) {
    courseInViewer = course;
    selectedVideo = null;
    showCourseViewer = true;
  }

  function closeCourseViewer() {
    courseInViewer = null;
    selectedVideo = null;
    showCourseViewer = false;
  }

  function playVideo(video: Video) {
    selectedVideo = video;
  }
  function handleKeydown(event: KeyboardEvent, callback: () => void) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      callback();
    }
  }  // Voting functions (copied from MyCourses.svelte)
  async function upVote(course: Course, video: Video) {
    let courseCode = course.code;
    let videoId = video.id;
    
    // Check if user is logged in
    if (!isLoggedIn) {
      alert('Please log in to vote on videos.');
      return;
    }
    
    try {
      // If already upvoted, revert the upvote
      if (isUpvoted(videoId)) {
        await revertVote(course, video, true);
        return;
      }
      
      // If downvoted, revert the downvote first
      if (isDownvoted(videoId)) {
        await revertVote(course, video, false);
      }
      
      const response = await fetch(`/api/vote/${courseCode}/${videoId}/upvote`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const result = await response.json();
      
      if (response.ok) {
        console.log("Upvote successful:", result.message);
        await refreshCourseData(courseCode);
      } else {
        console.error("Upvote failed:", result.error);
      }
    } catch (e) {
      console.log("Error Occurred - ", e);
    }
  }  async function downVote(course: Course, video: Video) {
    let courseCode = course.code;
    let videoId = video.id;
    
    // Check if user is logged in
    if (!isLoggedIn) {
      alert('Please log in to vote on videos.');
      return;
    }
    
    try {
      // If already downvoted, revert the downvote
      if (isDownvoted(videoId)) {
        await revertVote(course, video, false);
        return;
      }
      
      // If upvoted, revert the upvote first
      if (isUpvoted(videoId)) {
        await revertVote(course, video, true);
      }
      
      const response = await fetch(`/api/vote/${courseCode}/${videoId}/downvote`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const result = await response.json();
      
      if (response.ok) {
        console.log("Down vote successful:", result.message);
        await refreshCourseData(courseCode);
      } else {
        console.error("Downvote failed:", result.error);
      }
    } catch (e) {
      console.log("Error Occurred - ", e);
    }
  }

  async function revertVote(course: Course, video: Video, upOrDown: boolean){
    let courseCode = course.code;
    let videoId = video.id;
    let revert = '';
    try {
      if(upOrDown){
        revert = "revert_upvote";
      } else{
        revert = "revert_downvote";
      }
      const response = await fetch(`/api/vote/${courseCode}/${videoId}/${revert}`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const result = await response.json();      if (response.ok) {
        console.log("Revert vote successful:", result.message," - ", revert);
        await refreshCourseData(courseCode);
      } else {
        console.error("Revert vote failed:", result.error);
      }
    } catch (e) {
      console.log("Error Occurred - ", e);
    }
  }  async function refreshCourseData(courseCode: string) {
    try {
      // Get fresh video data for the course
      const response = await fetch(`/api/videos/${courseCode}`);
      if (!response.ok) throw new Error('Failed to fetch videos');
      const freshVideos = await response.json();
      
      // Update courseInViewer if it is the same course
      if (courseInViewer && courseInViewer.code === courseCode) {
        courseInViewer = { ...courseInViewer, videos: freshVideos };
      }
      
      // Update allCourses to keep data consistent
      allCourses = allCourses.map(course => {
        if (course.code === courseCode) {
          return { ...course, videos: freshVideos };
        }
        return course;
      });

      // Refresh user votes to update UI state
      if (isLoggedIn) {
        await getUserVotes();
      }
    } catch (error) {
      console.error('Error refreshing course data:', error);
    }
  }

  // Get user votes from backend
  async function getUserVotes() {
    try {
      const res = await fetch('/api/user_votes');
      const voteData = await res.json();
      userVotes = voteData;
    } catch(e) {
      console.log("Error Occurred - ", e);
    }
  }

  // Helper functions to check vote state
  function isUpvoted(videoId: string): boolean {
    return userVotes.upvote?.includes(videoId) || false;
  }

  function isDownvoted(videoId: string): boolean {
    return userVotes.downvote?.includes(videoId) || false;
  }
</script>

<!--main container that holds everything -->
<div class="course-catalog-page">
  <main>
    <!--page title at the top -->
    <header>
      <h1>Course Catalog</h1>
      <h2>Search for Computer Science Courses at UC Davis.</h2>
    </header>

    <!--search box that filters courses as you type using the bind:value -->
    <section class="search-container">
      <div class="search-input">
        <input 
          type="text" 
          placeholder="Search for courses (e.g. ECS 162)" 
          bind:value={searchPhrase}
        />
      </div>
    </section>

    <!-- Always show the course catalog, even if not logged in -->
    {#if loading}
      <div class="loading">Loading courses...</div>
    {:else if error}
      <div class="error">Error: {error}</div>
    {:else}      <section class="grid">
        {#each filteredCourses as course, i}
          <div class="cell">
            <button 
              class="course-btn"
              on:click={() => showCourseDetails(course)}
            >
              {#if course.videos && course.videos.length > 0}
                <img class="landing-thumb" src={`https://i.ytimg.com/vi/${course.videos[0].id}/hqdefault.jpg`} alt={course.videos[0].title} />
              {/if}
              <div class="landing-keywords">
                {#each course.keywords?.slice(0, 2) as keyword}
                  <span class="landing-keyword-tag">{keyword}</span>
                {/each}
              </div>
              <div class="landing-title-row">
                <span class="landing-code landing-code-black">{course.code}</span>
              </div>
              <div class="landing-title">{course.title}</div>
            </button>
            <button class="add-course-btn" on:click={() => addCourse(course)}>Add to Your Courses</button>
          </div>
        {/each}
      </section>
    {/if}
  </main>

  <!--popup that shows when you click a course - only visible if a course is selected -->
  {#if showCourseViewer && courseInViewer}
    <!--role="button" and tabindex="0" make this div keyboard-focusable -->
    <div 
      class="course-viewer" 
      on:click={closeCourseViewer}
      role="button"
      tabindex="0"
      on:keydown={(e) => handleKeydown(e, closeCourseViewer)}
      aria-label="Close course details"
    >
      <!--stopPropagation here prevents clicks inside from closing the popup -->
      <div class="course-viewer-content" on:click|stopPropagation
      role="button"
      tabindex="0"
      on:keydown={(e) => handleKeydown(e, closeCourseViewer)}
      aria-label="Close course details"
      >
        <!--x button in top right to close popup -->
        <button class="close-viewer-btn" on:click={closeCourseViewer}>×</button>

        <div class="viewer-header-card">
          <div class="viewer-code">{courseInViewer.code}</div>
          <div class="viewer-title">{courseInViewer.title}</div>
          <div class="viewer-description">{courseInViewer.description}</div>
        </div>
        
        <!--section for youtube videos related to the course -->
        <div class="videos-section">
          <!--shows the currently playing video if one is selected -->
          <!--iframe embeds youtube video player; allow="" lists permitted features -->
          {#if selectedVideo}
            <div class="video-player">
              <iframe
                width="100%"
                height="400"
                src={`https://www.youtube.com/embed/${selectedVideo.id}`}
                title={selectedVideo.title}
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
              <div class="video-info">
                <h5>{selectedVideo.title}</h5>
                <p class="channel">{selectedVideo.channel}</p>
              </div>
            </div>
          {/if}

          <!--grid of video thumbnails;clicking one makes it play above -->
          <h4>Related Videos</h4>
          <div class="videos-grid">
            {#each courseInViewer.videos as video}
              <div class="video-card-container">
                <button 
                  class="video-card"
                  on:click={() => playVideo(video)}
                >
                  <!--gets video thumbnail from youtube using video ID -->
                  <img src={`https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`} alt={video.title} />
                  <div class="video-info">
                    <h5>{video.title}</h5>
                    <p class="channel">{video.channel}</p>
                  </div>                </button>                <div class="vote-controls-centered">
                  <button 
                    class="upvote-btn-small {isUpvoted(video.id) ? 'voted' : ''}" 
                    on:click|stopPropagation={() => upVote(courseInViewer, video)}
                  >
                    👍
                  </button>
                  <div class="vote-count">{video.up_vote}</div>
                  <button 
                    class="downvote-btn-small {isDownvoted(video.id) ? 'voted' : ''}" 
                    on:click|stopPropagation={() => downVote(courseInViewer, video)}
                  >
                    👎
                  </button>
                  <div class="vote-count">{video.down_vote}</div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>