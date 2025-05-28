<script lang="ts">
  // Search for Courses page logic will go here
</script>

<main>
  <header>
    <h1>Search Courses</h1>
  </header>  <section class="search-container">
    <div class="search-input">
      <input type="text" placeholder="Search for courses (e.g. ECS 162)" />
      <button>Search</button>
    </div>
  </section>
  <section class="grid">
    <div class="cell color-1">
      <h3>Computer Science</h3>
      <p>All CS courses</p>
    </div>
    <div class="cell color-2">
      <h3>Engineering</h3>
      <p>All Engineering courses</p>
    </div>
    <div class="cell color-3">
      <h3>Biology</h3>
      <p>All Biology courses</p>
    </div>
    <div class="cell color-1">
      <h3>Mathematics</h3>
      <p>All Math courses</p>
    </div>
    <div class="cell color-2">
      <h3>Physics</h3>
      <p>All Physics courses</p>
    </div>
    <div class="cell color-3">
      <h3>Chemistry</h3>
      <p>All Chemistry courses</p>
    </div>
    <div class="cell color-1">
      <h3>Economics</h3>
      <p>All Economics courses</p>
    </div>
    <div class="cell color-2">
      <h3>Humanities</h3>
      <p>All Humanities courses</p>
    </div>
    <div class="cell color-3">
      <h3>Arts</h3>
      <p>All Arts courses</p>
    </div>
  </section>
</main>

<style>
  main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  header {
    width: 100%;
    padding: 2rem 0;
    text-align: center;
  }
  
  h1 {
    margin: 0;
    color: var(--color-text);
  }

  .search-container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto 1rem auto;
    padding: 0 1rem;
  }

  .search-input {
    display: flex;
    gap: 0.5rem;
  }

  input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 4px;
    background: rgba(255,255,255,0.1);
    color: var(--color-text);
    font-size: 1rem;
  }

  input::placeholder {
    color: rgba(255,255,255,0.5);
  }

  button {
    background-color: var(--color-3);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.75rem 1.5rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  button:hover {
    background-color: var(--color-2);
  }
</style>
