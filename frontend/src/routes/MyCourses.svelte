<script lang="ts">
  // My Courses page logic will go here
</script>

<main>
  <header>
    <h1>My Courses</h1>
  </header>
  <section class="grid">
    <div class="cell color-1">1</div>
    <div class="cell color-2">2</div>
    <div class="cell color-3">3</div>
    <div class="cell color-1">4</div>
    <div class="cell color-2">5</div>
    <div class="cell color-3">6</div>
    <div class="cell color-1">7</div>
    <div class="cell color-2">8</div>
    <div class="cell color-3">9</div>
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
