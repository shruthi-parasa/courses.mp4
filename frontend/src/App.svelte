<script lang="ts">
  import { onMount } from 'svelte';

  let apiKey: string = '';

  onMount(async () => {
    try {
      const res = await fetch('/api/key');
      const data = await res.json();
      apiKey = data.apiKey;
    } catch (error) {
      console.error('Failed to fetch API key:', error);
    }
  }); 
</script>

<main>
  <!-- Blank page, background color retained by CSS -->
</main>

<style>
  main {
    min-height: 100vh;
    background: #fff;
    /* You can adjust the background color here if needed */
  }
  body {
    margin: 0;
    padding: 0;
  }
  /* Retain or adjust background color as needed */
</style>
