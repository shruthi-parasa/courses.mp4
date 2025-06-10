<script lang="ts">
  // My Courses page logic will go here
  import {getUser} from '../get_user';
  let showSidepanel = false;
  // let isLoggedIn = false; // TODO: need to change this after implementing dex
  let courses: { code: string; title: string; description: string }[] = [];
  let loading = true;
  let error: string | null = null;
  let favoriteCourses = new Set<string>();
  let allCourses: any[] = [];
  
  let userCourseList: any[] = [];

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

  //login and logout functions manual for now, will change after implementing dex
  function handleLogin() {
    window.location.href = '/login';
    //isLoggedIn = true;
    //load favorites from local storage and fetch courses
    loadFavorites();
    fetchAllCourses();
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

  import { onMount } from 'svelte';
  onMount(() => {
    loadFavorites();
    fetchAllCourses();
    let username = getUser();
    if (username != null){
      getUserCourses();
    } 
  });
  
  async function fetchAllCourses() {
    try{
      const res = await fetch('/api/test_courses');
      const courseData = await res.json();
      allCourses = Object.entries(courseData).map(([code, data]: [string, any]) => ({
        code,
        title: data.title,
        description: data.description,
        keywords: data.keywords,
        videos: data.videos
      }));      
      
      console.log("Getting all courses...", allCourses);

    } catch (e) {
      error = e instanceof Error ? e.message : 'An error occurred';
      loading = false;
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
      let filteredUserCourses = allCourses.filter(course => courses.includes(course.code));
      userCourseList = filteredUserCourses;
      loading = false;
    } catch (e) {
      console.error('Error fetching courses:', e);
      loading = false;
    }
  }

  async function removeCourse(courseCode: any) {
    loading = true;
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
        // removes from local array immediately
        // courses = courses.filter(course => course !== courseCode);
        await getUserCourses();
      } else {
        message = result.error; 
      }
    } catch (err) {
      console.error('Error removing course:', err);
    } finally {
      loading = false;
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
            {#each userCourseList as course, i}
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
                <h3>Hello</h3>       
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
              <button 
                class="video-card"
                on:click={() => playVideo(video)}
              >
                <!--gets video thumbnail from youtube using video ID -->
                <img src={`https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`} alt={video.title} />
                <div class="video-info">
                  <h5>{video.title}</h5>
                  <p class="channel">{video.channel}</p>
                </div>
              </button>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>