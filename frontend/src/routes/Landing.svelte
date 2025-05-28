<script lang="ts">
  // Landing page logic will go here
</script>

<main>    <header>
      <h1>Landing Page</h1>
    </header>    <section class="grid">
      <div class="cell color-1">
        <h3>Welcome</h3>
        <p>Find course videos</p>
      </div>
      <div class="cell color-2">
        <h3>Browse</h3>
        <p>By department</p>
      </div>
      <div class="cell color-3">
        <h3>Search</h3>
        <p>By course code</p>
      </div>
      <div class="cell color-1">
        <h3>Popular</h3>
        <p>Top courses</p>
      </div>
      <div class="cell color-2">
        <h3>Recent</h3>
        <p>New videos</p>
      </div>
      <div class="cell color-3">
        <h3>Featured</h3>
        <p>Staff picks</p>
      </div>
      <div class="cell color-1">
        <h3>About</h3>
        <p>Learn more</p>
      </div>
      <div class="cell color-2">
        <h3>Help</h3>
        <p>Support</p>
      </div>
      <div class="cell color-3">
        <h3>Feedback</h3>
        <p>Contact us</p>
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
</style>
