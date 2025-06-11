<script lang="ts">
  // Landing page logic will go here
  import { onMount } from 'svelte';

  //replicates the SearchCourses.svelte interface
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
  }  let courses: Course[] = [];
  let loading = true;
  let error: string | null = null;
  let selectedCourse: Course | null = null;
  let showViewer: boolean = false;
  let selectedVideo: Video | null = null;

  //fetch 3 courses with video data for landing page to highlight the landing page
  async function fetchLandingCourses() {
    try {
      const response = await fetch('/api/test_courses');
      if (!response.ok) throw new Error('Failed to fetch courses');
      const courseData = await response.json();
      //first three courses for display
      courses = Object.entries(courseData).slice(0, 3).map(([code, data]: [string, any]) => ({
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
  }  onMount(() => {
    fetchLandingCourses();
  });

  //opens the course viewer modal when a course card is clicked
  //sets the selected course, clears any previously selected video, and shows the viewer overlay
  function openViewer(course: Course) {
    selectedCourse = course;
    selectedVideo = null; 
    showViewer = true;
  }

  //closes the course viewer modal
  //clears the selected course and video, and hides the viewer overlay
  function closeViewer() {
    selectedCourse = null;
    selectedVideo = null;
    showViewer = false;
  }

  //sets the currently selected video to play in the video player
  //called when clicking a video thumbnail in the course viewer
  function playVideo(video: Video) {
    selectedVideo = video;
  }
  function handleCardKeydown(event: KeyboardEvent, course: Course) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      openViewer(course);
    }  }
</script>

<div class="landing-page">
<main>
  <header>
    <h1>Courses.MP4</h1>
    <h2>Discover curated Youtube videos for courses offered at University of California, Davis.</h2>
  </header>
  <!-- 
  <section class="grid">
    <div class="cell color-1">
      <h3>Popular</h3>
      <p>View top-rated educational videos for UC Davis courses</p>
    </div>
    <div class="cell color-2">
      <h3>Search</h3>
      <p>Find resources for specific courses by course code</p>
    </div>
    <div class="cell color-3">
      <h3>About</h3>
      <p>Learn more about Courses.MP4 and our mission</p>
    </div> -->
  <!-- <section class="search-bar">
    <div class="search-input">
      <input
        type="text"
        placeholder="Search for a Course (e.g. ECS 162)"
        bind:value={search}
      />
      <button>Search</button>
    </div>
  </section> -->


  <!--below code similar to search courses/course catalog page code-->  <section class="grid">
    {#if loading}
      <div>Loading...</div>
    {:else if error}
      <div class="error">{error}</div>
    {:else}
      {#each courses as course}
        <div class="cell">
          <button 
            class="course-btn"
            on:click={() => openViewer(course)}
            on:keydown={(e) => handleCardKeydown(e, course)}
            aria-label={`View details for ${course.code} - ${course.title}`}
          >
            {#if course.videos && course.videos.length > 0}
              <img class="landing-thumb" src={`https://i.ytimg.com/vi/${course.videos[0].id}/hqdefault.jpg`} alt={course.videos[0].title} />
            {/if}
            <div class="landing-keywords">
              {#each course.keywords.slice(0, 2) as keyword}
                <span class="landing-keyword-tag">{keyword}</span>
              {/each}
            </div>
            <div class="landing-title-row">
              <span class="landing-code landing-code-black">{course.code}</span>
            </div>
            <div class="landing-title">{course.title}</div>
          </button>
        </div>
      {/each}
    {/if}
  </section>

  {#if showViewer && selectedCourse}
    <div 
      class="course-viewer" 
      on:click={closeViewer}
      role="button"
      tabindex="0"
      aria-label="Close course details"
    >
      <div class="course-viewer-content" on:click|stopPropagation
        role="button"
        tabindex="0"
        aria-label="Close course details"
      >
        <button class="close-viewer-btn" on:click={closeViewer}>×</button>
        <div class="viewer-header-card">
          <div class="viewer-code">{selectedCourse.code}</div>
          <div class="viewer-title">{selectedCourse.title}</div>
          <div class="viewer-description">{selectedCourse.description}</div>
        </div>
        <div class="videos-section">
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
          <h4>Related Videos</h4>
          <div class="videos-grid">
            {#each selectedCourse.videos as video}
              <div class="video-card-container">
                <button 
                  class="video-card"
                  on:click={() => playVideo(video)}
                >
                  <img src={`https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`} alt={video.title} />                  <div class="video-info">
                    <h5>{video.title}</h5>
                    <p class="channel">{video.channel}</p>
                  </div>
                </button>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/if}
</main>
</div>

<!-- All styling is handled by app.scss -->
