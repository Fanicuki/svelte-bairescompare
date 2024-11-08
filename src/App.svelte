<script lang="ts">
  import './assets/scripts.ts'

  function searchProduct(): void {
    alert("Buscando producto...");
  }

  function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === "Enter") {
      const searchButton = document.getElementById("searchButton") as HTMLButtonElement;
      searchButton.click();
    }
  }

  // Add this onMount import at the top of your script
  import { onMount } from 'svelte';

  onMount(() => {
    document.addEventListener("keydown", handleKeyDown);

    // Clean up the event listener when the component is destroyed
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  });
</script>

<svelte:head>
  <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
</svelte:head>

<div class="navbar">
  <a href="#">BairesCompare</a>
</div>
<div class="container">
  <img
    class="bairescompare_icon"
    src="bairescompare_icon.png"
    alt="BairesComare_icon"
  /><br />
  <div class="search-container">
    <input type="text" id="search-input" placeholder="Buscar producto..." />
  </div>
  <button
    class="button-62"
    role="button"
    on:click={searchProduct}
    id="searchButton">Buscar</button
  >
  <hr class="dashed" />
  <div id="loading-spinner" class="spinner" style="display: none;"></div>
  <ul id="product-list"></ul>
</div>

<div id="modal" class="modal">
  <div class="modal-content">
    <span class="close" on:click={() => closeModal()}>&times;</span>  
    <p>Por favor, ingresa el nombre de un producto.</p>
  </div>
</div>

<footer class="footer">
  <ul class="social-icon">
    <li class="social-icon__item">
      <a class="social-icon__link" href="https://wa.me/+541170252595">
        <ion-icon name="logo-whatsapp"></ion-icon>
      </a>
    </li>
    <li class="social-icon__item">
      <a class="social-icon__link" href="https://crmtec1vl.blogspot.com/">
        <ion-icon name="school"></ion-icon>
      </a>
    </li>
    <li class="social-icon__item">
      <a class="social-icon__link" href="https://www.instagram.com/patowica/">
        <ion-icon name="logo-instagram"></ion-icon>
      </a>
    </li>
  </ul>
  <p>&copy;2024 BairesCompare | Todos los derechos reservados</p>
</footer>