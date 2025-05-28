<script lang="ts">
  // My Courses page logic will go here
</script>

<main>
  <header>
    <h1>My Courses</h1>
  </header>  <section class="grid">
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
