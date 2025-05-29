<script lang="ts">
  // Landing page logic will go here
  
  
  let search = '';
  // manually added courses for display/testing purposes
  let courses = [
    {
      name: 'ANT 122B: Anthropology of Capitalism',
      image: '', // Placeholder for now
      duration: '11h 20m',
      created: '2 months ago',
      tags: ['ANT', 'Upper Division'],
      saves: 23
    },
    {
      name: 'DES 001: Intro to Design',
      image: '',
      duration: '70h 45m',
      created: '2 months ago',
      tags: ['Design', 'Prerequisites'],
      saves: 12
    },
    {
      name: 'ECS 132: Statistical Modeling',
      image: '',
      duration: '18h 20m',
      created: '2 months ago',
      tags: ['Data Science', 'Computer Science'],
      saves: 12
    },
    {
      name: 'COM 001: Public Speaking',
      image: '',
      duration: '11h 20m',
      created: '2 months ago',
      tags: ['Communication', 'General Education'],
      saves: 3
    }
  ];
  $: filteredCourses = courses.filter(course => course.name.toLowerCase().includes(search.toLowerCase()));
</script>

<main>
  <header>
    <h1>Courses.MP4</h1>
    <h2>Discover curated Youtube playlists for courses offered at University of California, Davis.</h2>
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
  <section class="search-bar">
    <div class="search-input">
      <input
        type="text"
        placeholder="Search for a Course (e.g. ECS 162)"
        bind:value={search}
      />
      <button>Search</button>
    </div>
  </section>
  <section class="course-list">
    {#each filteredCourses as course}
      <div class="course-card">
        <div class="course-image">
          {#if course.image} <!--for when we have images to add-->
            <img src={course.image} alt="Course image" />
          {:else} <!--placeholder for when we don't have images to add-->
            <div class="image-placeholder"></div>
          {/if}
        </div>
        <div class="course-tags"> 
          {#each course.tags as tag} <!--tags extracted from the manually added courses-->
            <span class="tag">{tag}</span> 
          {/each}
        </div>
        <div class="course-title">{course.name}</div>
        <div class="course-data"> <!--duration, created, and saves for now, can add more data later-->
          {course.duration} · {course.created} · <span class="star">⭐ {course.saves}</span>
        </div>
      </div>
    {/each}
  </section>
</main>

<!-- All styling is handled by app.scss -->
