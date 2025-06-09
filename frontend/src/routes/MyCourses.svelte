<script lang="ts">
  // My Courses page logic will go here
  import {getUser} from '../get_user';
  let showSidepanel = false;
  // let isLoggedIn = false; // TODO: need to change this after implementing dex
  let courses: { code: string; title: string; description: string }[] = [];
  let loading = true;
  let error: string | null = null;
  let favoriteCourses = new Set<string>();

  //login and logout functions manual for now, will change after implementing dex
  function handleLogin() {
    window.location.href = '/login';
    //isLoggedIn = true;
    //load favorites from local storage and fetch courses
    loadFavorites();
    fetchCourses();
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

  async function fetchCourses() {
    loading = true;
    try {
      //fetch the course codes from the backend
      const response = await fetch('/api/courses_list');
      if (!response.ok) throw new Error('Failed to fetch courses');
      const courseCodes = await response.json();
      
      //fetch the details for each course
      const courseDetails = await Promise.all(
        courseCodes.map(async (code: string) => {
          const detailResponse = await fetch(`/api/courses/${code}`);
          if (!detailResponse.ok) throw new Error(`Failed to fetch details for ${code}`);
          const details = await detailResponse.json();
          return {
            code,
            title: details.title,
            description: details.description
          };
        })
      );
      
      courses = courseDetails;
      loading = false;
    } catch (e) {
      error = e instanceof Error ? e.message : 'An error occurred';
      loading = false;
    }
  }

  import { onMount } from 'svelte';
  onMount(() => {
    loadFavorites();
    let username = getUser();
    if (username != null) fetchCourses();
  });
  //filtering courses based on favorites, so my courses page only shows favorited courses
  $: favoritedCourses = courses.filter(course => favoriteCourses.has(course.code));

  //trigger the sidepanel for the account info
  function toggleSidepanel() {
    showSidepanel = !showSidepanel;
  }
</script>

<div class="my-courses-page">
<main>
  <header>
    <h1>My Courses</h1>
  </header>
  <div class="account-btn-row">
    <button class="account-btn" on:click={toggleSidepanel}>
      Account
    </button>
  </div>
  <div class="content-wrapper">
    {#await getUser()}
    <p>Loading...</p>
    {:then username}
    {#if typeof username !== "undefined"}
    {:else if username == null}
      <div class="login-prompt left-align">Please log in to view your courses.</div>
    {:else if loading}
      <div class="loading">Loading your courses...</div>
    {:else if error}
      <div class="error">Error: {error}</div>
    {:else if favoritedCourses.length === 0}
      <!--no courses msg-->
      <div class="no-courses">You have not favorited any courses yet.</div>
    {:else}
      <section class="grid">
        {#each favoritedCourses as course, i}
          <div class="cell color-{(i % 3) + 1}"> <!--color is changed to a different color for each course-->
            <h3>{course.code}</h3>
            <p>{course.title}</p>
          </div>
        {/each}
      </section>
    {/if}
    {#if showSidepanel}
      <aside class="sidepanel">
        <div class="sidepanel-header">
          <h2>Account</h2>
          <button class="close-btn" on:click={toggleSidepanel}>×</button>
        </div>
        <div class="sidepanel-content">
          {#if username != null}
            <div class="account-info">
              <h3>Hello</h3>
              <button class="logout-btn" on:click={handleLogout}>
                Logout
              </button>
            </div>
          {:else}
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

<!-- All styling is now handled by app.scss -->
