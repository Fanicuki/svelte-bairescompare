<script lang="ts">
  import { onMount } from "svelte";

  function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === "Enter") {
      const searchButton = document.getElementById(
        "searchButton"
      ) as HTMLButtonElement;
      searchButton.click();
    }
  }

  // Utiliza onMount para gestionar el evento keydown
  onMount(() => {
    document.addEventListener("keydown", handleKeyDown);

    // Limpia el evento cuando el componente se destruye
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  });

  document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal") as HTMLElement;
    modal.style.display = "none";
  });

  async function searchProduct(): Promise<void> {
    const queryInput = document.getElementById(
      "search-input"
    ) as HTMLInputElement;
    const query = queryInput.value.toLowerCase();
    const productList = document.getElementById("product-list") as HTMLElement;
    const spinner = document.getElementById("loading-spinner") as HTMLElement;
    const modal = document.getElementById("modal") as HTMLElement;

    productList.innerHTML = "";

    if (!query) {
      modal.style.display = "flex";
      return;
    }

    // Mostrar la rueda de carga
    spinner.style.display = "block";

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/search?query=${query}`
      );

      if (!response.ok) {
        console.error("Error fetching data:", response.statusText);
        return;
      }

      const products: Array<{
        image: string;
        name: string;
        price: number;
        store: string;
        url: string;
      }> = await response.json();

      // Añadir depuración aquí
      console.log("Productos recibidos:", products);

      products.forEach((product) => {
        const li = document.createElement("li");

        // Imagen del producto
        const img = document.createElement("img");
        img.src = product.image;
        img.alt = product.name.replace(/\b\w/g, (char) => char.toUpperCase());
        img.style.width = "150px";
        img.style.height = "150px";
        li.appendChild(img);

        // Espacio entre imagen del producto y el texto
        li.appendChild(document.createTextNode(" "));

        // Link al producto
        const a = document.createElement("a");
        a.href = product.url;
        a.target = "_blank";
        a.textContent = `${product.name.replace(/\b\w/g, (char) => char.toUpperCase())} - $${product.price.toFixed(2)} - ${product.store}`;
        li.appendChild(a);

        // Espacio entre el texto y el logo del supermercado
        li.appendChild(document.createTextNode(" "));

        // Imagen del logo del supermercado
        const storeLogo = document.createElement("img");
        if (product.store === "Carrefour") {
          storeLogo.src = "../static/carrefour_logo.png";
        } else if (product.store === "Día") {
          storeLogo.src = "../static/dia_logo.png";
        }
        storeLogo.alt = `${product.store} Logo`;
        storeLogo.style.width = "20%";
        storeLogo.style.height = "20%";
        li.appendChild(storeLogo);

        productList.appendChild(li);
      });
    } catch (error) {
      console.error("Error:", error);
    } finally {
      spinner.style.display = "none";
    }
  }

  function closeModal(): void {
    const modal = document.getElementById("modal") as HTMLElement;
    modal.style.display = "none";
  }

  
</script>

<svelte:head>
  <script
    type="module"
    src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"
  ></script>
  <script
    nomodule
    src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"
  ></script>
</svelte:head>

<div class="navbar">
  <a href="#">BairesCompare</a>
</div>
<div class="container">
  <img
    class="bairescompare_icon"
    src="../static/bairescompare_icon.png"
    alt="BairesCompare_icon"
  /><br />
  <div class="search-container">
    <input type="text" id="search-input" placeholder="Buscar producto..." />
  </div>
  <button class="button-62" on:click={searchProduct} id="searchButton"
    >Buscar</button
  >
  <hr class="dashed" />
  <div id="loading-spinner" class="spinner" style="display: none;"></div>
  <ul id="product-list"></ul>
</div>

<div id="modal" class="modal">
  <div class="modal-content">
    <button type="button" on:click={() => closeModal()} aria-label="Close"
      >&times;</button
    >
    <p>Por favor, ingresa el nombre de un producto.</p>
  </div>
</div>

<footer class="footer">
  <ul class="social-icon">
    <li class="social-icon__item">
      <a
        class="social-icon__link"
        href="https://wa.me/+541170252595"
        aria-label="Contactar vía WhatsApp"
      >
        <ion-icon name="logo-whatsapp"></ion-icon>
      </a>
      <a
        class="social-icon__link"
        href="https://crmtec1vl.blogspot.com/"
        aria-label="Visitar blog de la escuela"
      >
        <ion-icon name="school"></ion-icon>
      </a>
      <a
        class="social-icon__link"
        href="https://www.instagram.com/patowica/"
        aria-label="Visitar Instagram de Patowica"
      >
        <ion-icon name="logo-instagram"></ion-icon>
      </a>
    </li>
  </ul>
  <p>&copy;2024 BairesCompare | Todos los derechos reservados</p>
</footer>
