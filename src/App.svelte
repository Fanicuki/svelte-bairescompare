<script lang="ts">
  import { onMount } from "svelte";
  import { parse } from "node-html-parser";

  const delay = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  async function fetchWithRetry(
    url: string,
    retries: number = 3
  ): Promise<string | null> {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await fetch(url);
        if (response.ok) return await response.text();
        console.error(
          `Error fetching ${url}: ${response.statusText} (Intento ${attempt})`
        );
      } catch (error) {
        console.error(`Error fetching ${url} (Intento ${attempt}):`, error);
      }
      await delay(1000); // Espera entre reintentos
    }
    return null;
  }

  function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === "Enter") {
      const searchButton = document.getElementById(
        "searchButton"
      ) as HTMLButtonElement;
      searchButton.click();
    }
  }

  async function searchProduct(): Promise<void> {
    const queryInput = document.getElementById("search-input") as HTMLInputElement;
    const query = queryInput.value.toLowerCase().trim();
    const productList = document.getElementById("product-list") as HTMLElement;
    const spinner = document.getElementById("loading-spinner") as HTMLElement;
    const modal = document.getElementById("modal") as HTMLElement;

    productList.innerHTML = "";

    if (!query) {
      modal.style.display = "flex";
      return;
    }

    spinner.style.display = "block";

    try {
      const diaBaseUrl = "https://diaonline.supermercadosdia.com.ar/almacen";
      const jumboBaseUrl = "https://www.jumbo.com.ar/almacen";

      const diaProducts: Array<{
        image: string | null;
        name: string;
        price: number;
        store: string;
        url: string;
      }> = [];

      const jumboProducts: Array<{
        image: string | null;
        name: string;
        price: number;
        store: string;
        url: string;
      }> = [];

      // Función para extraer productos de Día
      const extractDiaData = async () => {
        let currentPage = 1;
        let hasMorePages = true;

        while (hasMorePages) {
          const html = await fetchWithRetry(`${diaBaseUrl}?page=${currentPage}`);
          if (!html) break;

          const root = parse(html);
          const productContainers = root.querySelectorAll(".vtex-product-summary-2-x-container");

          if (productContainers.length === 0) {
            hasMorePages = false;
            break;
          }

          productContainers.forEach((product) => {
            const imageTag = product.querySelector(".vtex-product-summary-2-x-imageNormal");
            const nameTag = product.querySelector(".vtex-product-summary-2-x-productBrand");
            const priceTag = product.querySelector(".vtex-product-price-1-x-currencyContainer");

            if (nameTag && priceTag) {
              const name = nameTag.textContent.toLowerCase();
              const price = parseFloat(
                priceTag.textContent.replace("$", "").replace(".", "").replace(",", ".")
              );

              const regex = new RegExp(query, "i");
              if (regex.test(name)) {
                diaProducts.push({
                  image: imageTag ? imageTag.getAttribute("src") : null,
                  name,
                  price,
                  store: "Día",
                  url: diaBaseUrl,
                });
              }
            }
          });

          currentPage++;
        }
      };

      // Función para extraer productos de Jumbo
      const extractJumboData = async () => {
        let currentPage = 1;
        let hasMorePages = true;

        while (hasMorePages) {
          const html = await fetchWithRetry(`${jumboBaseUrl}?page=${currentPage}`);
          if (!html) break;

          const root = parse(html);
          const productContainers = root.querySelectorAll(".vtex-search-result-3-x-galleryItem");

          if (productContainers.length === 0) {
            hasMorePages = false;
            break;
          }

          productContainers.forEach((product) => {
            const nameTag = product.querySelector(".vtex-product-summary-2-x-productBrand");
            const priceTag = product.querySelector(".jumboargentinaio-store-theme-1dCOMij_MzTzZOCohX1K7w");

            if (nameTag && priceTag) {
              const name = nameTag.textContent.toLowerCase();
              const price = parseFloat(
                priceTag.textContent.replace("$", "").replace(".", "").replace(",", ".")
              );

              const regex = new RegExp(query, "i");
              if (regex.test(name)) {
                jumboProducts.push({
                  image: null, // Ignorar imágenes para Jumbo
                  name,
                  price,
                  store: "Jumbo",
                  url: jumboBaseUrl,
                });
              }
            }
          });

          currentPage++;
        }
      };

      // Ejecutar ambas extracciones
      await Promise.all([extractDiaData(), extractJumboData()]);

      // Fusionar y ordenar productos
      const products = [...diaProducts, ...jumboProducts].sort((a, b) => a.price - b.price);

      // Renderizar los productos
      products.forEach((product) => {
        const li = document.createElement("li");

        if (product.image) {
          const img = document.createElement("img");
          img.src = product.image;
          img.alt = product.name.replace(/\b\w/g, (char) => char.toUpperCase());
          img.style.width = "150px";
          img.style.height = "150px";
          li.appendChild(img);
        }

        const a = document.createElement("a");
        a.href = product.url;
        a.target = "_blank";
        a.textContent = `${product.name.replace(/\b\w/g, (char) => char.toUpperCase())} - $${product.price.toFixed(
          2
        )} - ${product.store}`;
        li.appendChild(a);

        productList.appendChild(li);
      });

      if (products.length === 0) {
        console.log("No se encontraron productos para la búsqueda.");
      }
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

  onMount(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  });
</script>

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
  <button class="button-62" on:click={searchProduct} id="searchButton">
    Buscar
  </button>
  <hr class="dashed" />
  <div id="loading-spinner" class="spinner" style="display: none;"></div>
  <ul id="product-list"></ul>
</div>

<div id="modal" class="modal">
  <div class="modal-content">
    <button type="button" on:click={closeModal}>&times;</button>
    <p>Por favor, ingresa el nombre de un producto.</p>
  </div>
</div>

<footer class="footer">
  <ul class="social-icon">
    <li class="social-icon__item">
      <!-- svelte-ignore a11y_consider_explicit_label -->
      <a class="social-icon__link" href="https://wa.me/+541170252595">
        <ion-icon name="logo-whatsapp"></ion-icon>
      </a>
      <!-- svelte-ignore a11y_consider_explicit_label -->
      <a class="social-icon__link" href="https://crmtec1vl.blogspot.com/">
        <ion-icon name="school"></ion-icon>
      </a>
      <!-- svelte-ignore a11y_consider_explicit_label -->
      <a class="social-icon__link" href="https://www.instagram.com/patowica/">
        <ion-icon name="logo-instagram"></ion-icon>
      </a>
    </li>
  </ul>
</footer>
