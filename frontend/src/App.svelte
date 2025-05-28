<script lang="ts">
  import { onMount } from 'svelte';
  import Landing from './routes/Landing.svelte';
  import MyCourses from './routes/MyCourses.svelte';
  import SearchCourses from './routes/SearchCourses.svelte';
  
  let apiKey: string = '';
  let currentPage = 'landing';

  onMount(async () => {
    try {
      const res = await fetch('/api/key');
      const data = await res.json();
      apiKey = data.apiKey;
    } catch (error) {
      console.error('Failed to fetch API key:', error);
    }
  });

  function navigateTo(page: string) {
    currentPage = page;
  }
</script>

<main>
  <nav>
    <ul>
      <li><button class:active={currentPage === 'landing'} on:click={() => navigateTo('landing')}>Home</button></li>
      <li><button class:active={currentPage === 'my-courses'} on:click={() => navigateTo('my-courses')}>My Courses</button></li>
      <li><button class:active={currentPage === 'search'} on:click={() => navigateTo('search')}>Search</button></li>
    </ul>
  </nav>

  <div class="content">
    {#if currentPage === 'landing'}
      <Landing />
    {:else if currentPage === 'my-courses'}
      <MyCourses />
    {:else if currentPage === 'search'}
      <SearchCourses />
    {/if}
  </div>

  <footer class="site-footer">
    <div class="footer-content">
      <div class="logo">Courses.MP4</div>
      <div class="links">
        <a href="#about">About</a>
        <a href="#privacy">Privacy</a>
        <a href="#terms">Terms</a>
        <a href="#contact">Contact</a>
      </div>
      <div class="copyright">© {new Date().getFullYear()} Courses.MP4 | UC Davis</div>
    </div>
  </footer>
</main>

<style>
  /* Use regular CSS with variables */
  main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  nav {
    background-color: var(--color-bg);
    border-bottom: 1px solid var(--color-3);
    padding: 0.5rem 1rem;
  }

  nav ul {
    display: flex;
    list-style: none;
    padding: 0;
    margin: 0;
    justify-content: center;
    gap: 1rem;
  }

  nav button {
    background: none;
    border: none;
    color: var(--color-text);
    font-size: 1rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: color 0.2s;
    border-radius: 4px;
  }

  nav button:hover {
    color: var(--color-1);
  }

  nav button.active {
    background-color: var(--color-3);
    color: white;
  }

  .content {
    flex: 1;
  }

  footer {
    padding: 1rem;
    font-size: 0.8rem;
    text-align: center;
    color: var(--color-text);
    opacity: 0.6;
  }
</style>
