<script lang="ts">
  import {getUser} from '../get_user';
  // Search for Courses page logic will go here
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
  let courses: Course[] = [];
  let loading = true;
  let error: string | null = null;
  let searchPhrase = '';
  let favoriteCourses = new Set<string>();
  let showCourseViewer: boolean = false;
  let courseInViewer: Course | null = null;
  let selectedVideo: Video | null = null;
 
  
  //Need to check the available coures against the user's current favorite and added courses
  //Only show class that aren't already a part of the user's storage
  import { onMount } from 'svelte';
  onMount(async () => {
    
    let username = await getUser();
    if (username != null){
      console.log("User is logged in - ", username);
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

  async function fetchCourses() {
    try {
      // Fetch test course data
      const response = await fetch('/api/test_courses');
      if (!response.ok) throw new Error('Failed to fetch courses');
      const courseData = await response.json();
      
      // Transform the data into our Course interface format
      courses = Object.entries(courseData).map(([code, data]: [string, any]) => ({
        code,
        title: data.title,
        description: data.description,
        keywords: data.keywords,
        videos: data.videos
      }));
      
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
    let courseCode = courseInfo;
    console.log("Fuck me - ", courseCode.code);
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
      
    } catch (err) {
      console.error('Error adding course:', err);
    }
  }

  // Load favorites and fetch courses when component mounts
  loadFavorites();
  fetchCourses();

  // Filtering courses based on search phrase
  $: filteredCourses = courses.filter(course => 
    course.code.toLowerCase().includes(searchPhrase.toLowerCase()) ||
    course.title.toLowerCase().includes(searchPhrase.toLowerCase()) ||
    course.description.toLowerCase().includes(searchPhrase.toLowerCase()) ||
    course.keywords.some(keyword => keyword.toLowerCase().includes(searchPhrase.toLowerCase()))
  );

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

    <!--loading while fetching courses, or error if something went wrong -->
    {#if loading}
      <div class="loading">Loading courses...</div>
    {:else if error}
      <div class="error">Error: {error}</div>
    {:else}
      <!--grid layout of course cards from our filtered course list -->
      <section class="grid">
        {#each filteredCourses as course, i}
          <div class="cell">
            <!--heart button that saves/removes course from favorites in localStorage -->
            <!--stopPropagation prevents the click from triggering the parent card's click -->
            <!-- aria-label helps screen readers tell users what this button does -->
            <!-- <div 
              class="favorite-btn" 
              class:favorited={favoriteCourses.has(course.code)}
              on:click|stopPropagation={() => triggerFavs(course.code)}
              role="button"
              tabindex="0"
              on:keydown={(e) => handleKeydown(e, () => triggerFavs(course.code))}
              aria-label="Favorite course"
            >
              {favoriteCourses.has(course.code) ? '❤️' : '🤍'}
            </div> -->

            <!--clickable card; view of the course -->
            <button 
              class="course-btn"
              on:click={() => showCourseDetails(course)}
            >
            <!--thumbnail image on course card like in landing page-->
            {#if course.videos && course.videos.length > 0}
              <img class="landing-thumb" src={`https://i.ytimg.com/vi/${course.videos[0].id}/hqdefault.jpg`} alt={course.videos[0].title} />
            {/if}
            <h3 class="course-code">{course.code}</h3>
            <p>{course.title}</p>
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