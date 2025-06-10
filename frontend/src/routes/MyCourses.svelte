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
  //STILL NEED TO DO FRONTEND DESIGN FOR THIS!! -> DONE check app.scss for styling
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
    } catch (e) {
      console.error('Error fetching courses:', e);
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

  //filtering courses based on favorites, so my courses page only shows favorited courses
  // $: favoritedCourses = courses.filter(course => favoriteCourses.has(course.code));

  //trigger the sidepanel for the account info
  function toggleSidepanel() {
    showSidepanel = !showSidepanel;
  }
</script>

<!--holds everything for the my courses page-->
<div class="my-courses-page">
<main>
  <!--page title at top-->
  <header>
    <h1>My Courses</h1>
  </header>

  <!--open account settings-->
  <div class="account-btn-row">
    <button class="account-btn" on:click={toggleSidepanel}>
      Account
    </button>
  </div>

  <!--all the main content-->
  <div class="content-wrapper">
    <!--courses the user has added in a grid-->
    <section class="my-courses-grid">
      {#each userCourseList as course, i}
        <!--card showing info for one course-->
        <div class="my-courses-card color-{(i % 3) + 1}">
          <button 
            class="course-btn"
            on:click={() => showCourseDetails(course)}
            >
          {#if course.videos && course.videos.length > 0}
            <img class="landing-thumb" src={`https://i.ytimg.com/vi/${course.videos[0].id}/hqdefault.jpg`} alt={course.videos[0].title} />
          {/if}
          <h3 class="course-code">{course.code ? course.code : course}</h3>
          {#if course.title}
            <p class="course-title">{course.title}</p>
          {/if}
          </button>
          <button class="remove-course-btn" on:click={() => removeCourse(course.code ? course.code : course)}>
            Remove Course
          </button>
        </div>
      {/each}
    </section>

    <!--is user logged in? and shows different things based on that-->
    {#await getUser()}
    <p>Loading...</p>
    {:then username}
    {#if typeof username !== "undefined"}
    {:else if username == null}
      <!--tells user they need to login to see their courses-->
      <div class="login-prompt left-align">Please log in to view your courses.</div>
    {:else if loading}
      <!--courses are being loaded-->
      <div class="loading">Loading your courses...</div>
    {:else if error}
      <!--problem getting the courses-->
      <div class="error">Error: {error}</div>
    <!-- {:else if favoritedCourses.length === 0} -->
      <!--hasnt favorited any courses yet-->
      <div class="no-courses">You have not favorited any courses yet.</div>
    {:else}
      <!-- <section class="grid">
        {#each favoritedCourses as course, i}
          <div class="cell color-{(i % 3) + 1}">
            <h3>{course.code}</h3>
            <p>{course.title}</p>
          </div>
        {/each}
      </section> -->
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
  </div>
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


<!-- All styling is now handled by app.scss -->
 