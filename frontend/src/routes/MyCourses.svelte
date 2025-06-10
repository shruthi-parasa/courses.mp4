<script lang="ts">
  // My Courses page logic will go here
  import {getUser} from '../get_user';
  import { onMount } from 'svelte';
  let showSidepanel = false;
  // let isLoggedIn = false; // TODO: need to change this after implementing dex
  let courses: { code: string; title: string; description: string }[] = [];
  let loading = true;
  let error: string | null = null;
  let favoriteCourses = new Set<string>();
  let allCourses: any[] = [];
  
  let userCourseList: any[] = [];

  let userVotes: any[] = [];

  interface Video {
    title: string;
    id: string;
    channel: string;
    thumbnail: string;
    video_url: string;
  }

  interface Course {
    code: string;
    title: string;
    description: string;
    keywords: string[];
    videos: Video[];
  }

  let showCourseViewer: boolean = false;
  let courseInViewer: Course | null = null;
  let selectedVideo: Video | null = null;

  onMount(async () => {
    loadFavorites();
    let username = await getUser();
    if (username != null){
      await getUserCourses();
      await fetchCourseInfo();
      await getUserVotes();
    } 
  });
  //login and logout functions manual for now, will change after implementing dex
  function handleLogin() {
    window.location.href = '/login';
    //isLoggedIn = true;
    //load favorites from local storage and fetch courses
    // loadFavorites();
    // fetchAllCourses();
  }

  function handleLogout() {
    window.location.href = '/logout';
    //isLoggedIn = false;
  }

  function loadFavorites() {
    const favs = localStorage.getItem('favoriteCourses');
    if (favs) {
      try {
        //parse the favorites from local storage and set them to the favoriteCourses set
        favoriteCourses = new Set(JSON.parse(favs));
      } catch {}
    }
  }

  //Fetch function does not work - Commented out in case original coder wants to fix - K. Nguyen
  // async function fetchCourses() {
  //   loading = true;
  //   try {
  //     //fetch the course codes from the backend
  //     const response = await fetch('/api/courses_list');
  //     if (!response.ok) throw new Error('Failed to fetch courses');
  //     const courseCodes = await response.json();
      
  //     //fetch the details for each course
  //     const courseDetails = await Promise.all(
  //       courseCodes.map(async (code: string) => {
  //         const detailResponse = await fetch(`/api/courses/${code}`);
  //         if (!detailResponse.ok) throw new Error(`Failed to fetch details for ${code}`);
  //         const details = await detailResponse.json();
  //         return {
  //           code,
  //           title: details.title,
  //           description: details.description
  //         };
  //       })
  //     );
      
  //     courses = courseDetails;
  //     loading = false;
  //   } catch (e) {
  //     error = e instanceof Error ? e.message : 'An error occurred';
  //     loading = false;
  //   }
  // }

  async function fetchCourseInfo() {
  try {
    // Get Title, Description, and Keywords from test_courses
    const res = await fetch('/api/test_courses');
    const courseData = await res.json();      
   
    let initialFetchCourses = Object.entries(courseData).map(([code, data]: [string, any]) => ({
      code,
      title: data.title,
      description: data.description,
      keywords: data.keywords
    }));
    
    let filteredCourses = initialFetchCourses.filter(course => userCourseList.includes(course.code));
    
    allCourses = await Promise.all(
      filteredCourses.map(async (course) => ({
        code: course.code,
        title: course.title,
        description: course.description,
        keywords: course.keywords,
        videos: await getVideos(course.code)
      }))
    );
    
    // Update userCourseList with the complete course objects - Includes prior info with videos with most up-to-date votes
    userCourseList = allCourses;   
  } catch (e) {
    error = e instanceof Error ? e.message : 'An error occurred';
    loading = false;
  }
}

async function getVideos(courseCode: any) {
  try {
    const videoRes = await fetch(`/api/videos/${courseCode}`);
    const videoData = await videoRes.json();
    return videoData;
  } catch(e) {
    console.log("Error occurred ", e);
    return []; 
  }
}
  //Does all information fetching for the user's courses and videos
  async function getUserCourses() {
    try {
      const response = await fetch('/api/user/courses', {
        method: 'GET',
        credentials: 'include', 
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      courses = await response.json();
      console.log("User courses - ", courses);
      userCourseList = courses;
      loading = false;
    } catch (e) {
      console.error('Error fetching courses:', e);
      loading = false;
    }
  }

  //Issue appered when removing courses after voting implementation - Fixed K. Nguyen
  async function removeCourse(courseCode: any) {
    let message = '';
    
    try {
      const response = await fetch('/api/user/courses/remove', {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          course: courseCode
        })
      });
      
      const result = await response.json();
      
      if (response.ok) {
        message = result.message;

        userCourseList = userCourseList.filter(course => 
          (course.code || course) !== courseCode
        );
        
        if (courseInViewer && courseInViewer.code === courseCode) {
          closeCourseViewer();
        }

      } else {
        message = result.error;
        console.error('Remove course failed:', message);
      }
    } catch (err) {
      console.error('Error removing course:', err);
    }
  }

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
  }

  //trigger the sidepanel for the account info
  function toggleSidepanel() {
    showSidepanel = !showSidepanel;
  }

  //------------VOTING SYSTEM----------------------
  async function getUserVotes(){
    try{
      const res = await fetch ('/api/user_votes');
      const voteData = await res.json();
      userVotes = voteData;
    } catch(e){
      console.log("Error Occurred - ", e);
    }
  }

  //Upvoting Function - Needs full course array and the specific video array
  async function upVote(course: any, video: any) {
  let courseCode = course.code;
  let videoId = video.id;
  try {
    const response = await fetch(`/api/vote/${courseCode}/${videoId}/upvote`, {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const result = await response.json();

    if (response.ok) {
      if(result.message === "Already upvoted"){
        await revertVote(course, video, true);
      } else{
        console.log("Upvote successful:", result.message);
        
        await refreshCourseData(courseCode);
        
        alert(result.message);
      }
    } else {
      console.error("Upvote failed:", result.error);
      alert(result.error || "Failed to upvote video");
    }
  } catch (e) {
    console.log("Error Occurred - ", e);
  }
}
  //Downvoting Function - Needs full course array and the specific video array
  async function downVote(course: any, video: any) {
    let courseCode = course.code;
    let videoId = video.id;
    
    try {
      const response = await fetch(`/api/vote/${courseCode}/${videoId}/downvote`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const result = await response.json();

      if (response.ok) {
        if(result.message === "Already downvoted"){
          await revertVote(course, video, false);
        } else{
          console.log("Down vote successful:", result.message);
          
          await refreshCourseData(courseCode);
          
          alert(result.message);
        }
      } else {
        console.error("Downvote failed:", result.error);
        alert(result.error || "Failed to downvote video");
      }
    } catch (e) {
      console.log("Error Occurred - ", e);
    }
  }

  //Main revert vote function, for the boolean - Reverting upvote is true, false for downvote
  async function revertVote(course: any, video: any, upOrDown: boolean){
    let courseCode = course.code;
    let videoId = video.id;
    let revert = '';
    try {
      //Upvote = 0
      if(upOrDown){
        revert = "revert_upvote";
      }
      //Downvote = 1
      else{
        revert = "revert_downvote";
      }
      const response = await fetch(`/api/vote/${courseCode}/${videoId}/${revert}`, {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      const result = await response.json();

      if (response.ok) {
        console.log("Revert vote successful:", result.message," - ", revert);
        
        await refreshCourseData(courseCode);
        
        alert(result.message);
      } else {
        console.error("Revert upvote failed:", result.error);
        alert(result.error || "Failed to revert up vote on video");
      }
    } catch (e) {
      console.log("Error Occurred - ", e);
    }
  }
  // refresh data for a course - made to specifically target re-rendering issues
  async function refreshCourseData(courseCode: string) {
    try {
      // Get fresh video data for the course
      const freshVideos = await getVideos(courseCode);
      
      // Update userCourseList
      userCourseList = userCourseList.map(course => {
        if (course.code === courseCode) {
          return { ...course, videos: freshVideos };
        }
        return course;
      });
      
      // Update courseInViewer if it is the same course
      if (courseInViewer && courseInViewer.code === courseCode) {
        courseInViewer = { ...courseInViewer, videos: freshVideos };
      }
    } catch (error) {
      console.error('Error refreshing course data:', error);
    }
  }

</script>

<!--main container that holds everything -->
<div class="my-courses-page">
  <main>
    <!--page title at the top -->
    <header>
      <h1>My Courses</h1>
      <h2>Your enrolled Computer Science courses at UC Davis.</h2>
    </header>

    <!--open account settings-->
    <div class="account-btn-row">
      <button class="account-btn" on:click={toggleSidepanel}>
        Account
      </button>
    </div>

    <!--loading while fetching courses, or error if something went wrong -->
    {#await getUser()}
      <div class="loading">Loading...</div>
    {:then username}
      {#if typeof username !== "undefined"}
        {#if loading}
          <!--courses are being loaded-->
          <div class="loading">Loading your courses...</div>
        {:else if error}
          <!--problem getting the courses-->
          <div class="error">Error: {error}</div>
        {:else if userCourseList.length === 0}
          <!--hasn't added any courses yet-->
          <div class="no-courses">You have not added any courses yet.</div>
        {:else}
          <!--grid layout of course cards from user's course list -->
          <section class="grid">
            {#each userCourseList as course}
              <div class="cell">
                <!--clickable card; view of the course -->
                <button 
                  class="course-btn"
                  on:click={() => showCourseDetails(course)}
                >
                  <!--thumbnail image on course card-->
                  {#if course.videos && course.videos.length > 0}
                    <img class="landing-thumb" src={`https://i.ytimg.com/vi/${course.videos[0].id}/hqdefault.jpg`} alt={course.videos[0].title} />
                  {/if}
                  
                  <!--keywords section-->
                  <div class="landing-keywords">
                    {#each course.keywords?.slice(0, 1) as keyword}
                      <span class="landing-keyword-tag">{keyword}</span>
                    {/each}
                  </div>
                  
                  <!--course code and title-->
                  <div class="landing-title-row">
                    <span class="landing-code landing-code-black">{course.code}</span>
                  </div>
                  <div class="landing-title">{course.title}</div>
                </button>
                
                <!--remove course button-->
                <button class="remove-course-btn" on:click={() => removeCourse(course.code ? course.code : course)}>
                  Remove Course
                </button>
              </div>
            {/each}
          </section>
        {/if}
      {:else if username == null}
        <!--tells user they need to login to see their courses-->
        <div class="login-prompt">Please log in to view your courses.</div>
      {/if}

      <!--panel that slides in from side for account stuff-->
      {#if showSidepanel}
        <aside class="sidepanel">
          <!--top part of sidepanel with title and close button-->
          <div class="sidepanel-header">
            <h2>Account</h2>
            <button class="close-btn" on:click={toggleSidepanel}>×</button>
          </div>

          <!--main part of sidepanel with account options-->
          <div class="sidepanel-content">
            {#if username != null}
              <!--logout button when user is logged in-->
              <div class="account-info">
                <h3>
                  Welcome Back {username}!
                </h3>       
                <button class="logout-btn" on:click={handleLogout}>
                  Logout
                </button>
              </div>
            {:else}
              <!--login button when user is not logged in-->
              <div class="login-section">
                <button class="login-btn" on:click={handleLogin}>
                  Login
                </button>
                <p class="login-note">Sign in to access your courses and progress!</p>
              </div>
            {/if}
          </div>
        </aside>
      {/if}
    {/await}
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
                  <img src={`https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`} alt={video.title} />
                  <div class="video-info">
                    <h5>{video.title}</h5>
                    <p class="channel">{video.channel}</p>
                  </div>
                </button>
                <!-- Add upvote button for each video in the grid -->
                <button 
                  class="upvote-btn-small" 
                  on:click|stopPropagation={() => upVote(courseInViewer, video)}
                >
                  👍
                </button>
                <button 
                  class="downvote-btn-small" 
                  on:click|stopPropagation={() => downVote(courseInViewer, video)}
                >
                  👎
                </button>
                <!-- Ignore Error squiggles, works fine! - K. Nguyen -->
                <div>upVote: {video.up_vote}</div>
                <div>Downvotes: {video.down_vote}</div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>