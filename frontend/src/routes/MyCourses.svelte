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
      const res = await fetch('/api/courses_list');
      const data = await res.json();
      console.log("Getting all courses...", data);
      allCourses = data;
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
      console.log("User Courses ", courses);
      userCourseList = courses;
      for(let i = 0; i<userCourseList.length;i++){
        const findAvailCourse = allCourses.find(course => course === userCourseList[i]);
        if(findAvailCourse){
          console.log("Class is within domain of user-courses (MongoDB) ", findAvailCourse);
          const videoRes = await fetch(`/api/videos/${findAvailCourse}`,{
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json'
            }
          });
          let videos = await videoRes.json();
          console.log("Videos for ", findAvailCourse, " - ", videos);
        }
      }
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
        courses = courses.filter(course => course !== courseCode);
      } else {
        message = result.error; 
      }
    } catch (err) {
      console.error('Error removing course:', err);
    } finally {
      loading = false;
    }
  }

  //filtering courses based on favorites, so my courses page only shows favorited courses
  $: favoritedCourses = courses.filter(course => favoriteCourses.has(course.code));

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
          <h3 class="course-code">{course.code ? course.code : course}</h3>
          {#if course.title}
            <p class="course-title">{course.title}</p>
          {/if}
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
    {:else if favoritedCourses.length === 0}
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
</div>

  <!-- <section class="grid">
    {#each courses as course}
    <div 
      class = "cell {course.color}"
      on:click={() => searchForCourse(course)}>
      <h3>{course.code}</h3>
      <p>{course.name}</p>
    </div>
    {/each}
    <div class="cell color-1">
      <h3>ECS 162</h3>
      <p>Web Programming</p>
    </div>
    <div class="cell color-2">
      <h3>ECS 150</h3>
      <p>Operating Systems</p>
    </div>
    <div class="cell color-3">
      <h3>MAT 108</h3>
      <p>Intro to Abstract Math</p>
    </div>
    <div class="cell color-1">
      <h3>PHY 9A</h3>
      <p>Classical Physics</p>
    </div>
    <div class="cell color-2">
      <h3>CHE 2A</h3>
      <p>General Chemistry</p>
    </div>
    <div class="cell color-3">
      <h3>BIS 2A</h3>
      <p>Intro Biology</p>
    </div>
    <div class="cell color-1">
      <h3>ECN 1A</h3>
      <p>Microeconomics</p>
    </div>
    <div class="cell color-2">
      <h3>PSC 1</h3>
      <p>General Psychology</p>
    </div>
    <div class="cell color-3">
      <h3>MUS 10</h3>
      <p>Music Theory</p>
    </div>
  </section>
</main>
</div>

{#if showModal && selectedCourse}
  <div class="modal-overlay" on:click={closeModal}>
    <div class="modal-content" on:click|stopPropagation>
      <div class="modal-header">
        <h2>{selectedCourse.code}: {selectedCourse.name}</h2>
        <button class="close-button" on:click={closeModal}>&times;</button>
      </div>
      <div class="modal-body">
        {#if selectedCourse.data && Array.isArray(selectedCourse.data)}
          <div class="vid-grid">
            {#each selectedCourse.data as video}
              <div class="vid-card">
                <div class="vid-thumbnail">
                  <img src={video.thumbnail} alt={video.title} />
                  <div class="play-overlay">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                      <path d="M8 5v14l11-7z"/>
                    </svg>
                  </div>
                </div>
                <div class="vid-info">
                  <h3 class="vid-title">{@html video.title}</h3>
                  <p class="vid-channel">{video.channel}</p>
                  <p class="vid-date">{new Date(video.publish_time).toLocaleDateString()}</p>
                  <a href={video.video_url} target="_blank" class="watch-button">
                    Watch Video
                  </a>
                </div>
              </div>
            {/each}
          </div>
        {:else}
          <p>Loading course details...</p>
        {/if}
      </div>
    </div>
  </div>
{/if} -->

<!-- All styling is now handled by app.scss -->
 