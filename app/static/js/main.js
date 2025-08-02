// Menu responsivo
const menuToggle = document.getElementById('menu-toggle');
const navLinks = document.getElementById('nav-links');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Carrossel
const track = document.querySelector(".carrossel-track");
const dotsContainer = document.querySelector(".carrossel-dots");

const originals = Array.from(track.children);
const visible = 4; // número de itens visíveis ao mesmo tempo
const totalSlides = originals.length;

// Clonar os primeiros itens para criar looping suave
for (let i = 0; i < visible; i++) {
    const clone = originals[i].cloneNode(true);
    track.appendChild(clone);
}

let currentSlide = 0;
let transitioning = false;

// Criar os botões de navegação (pontos)
for (let i = 0; i < totalSlides; i++) {
    const dot = document.createElement("button");
    if (i === 0) dot.classList.add("active");
    dot.addEventListener("click", () => {
        currentSlide = i;
        updateCarousel();
        resetAutoSlide();
    });
    dotsContainer.appendChild(dot);
}

const dots = dotsContainer.querySelectorAll("button");

// Atualiza a posição do carrossel
function updateCarousel() {
    const itemWidth = originals[0].offsetWidth + 25; // inclui gap
    track.style.transform = `translateX(-${currentSlide * itemWidth}px)`;

    dots.forEach(dot => dot.classList.remove("active"));
    if (dots[currentSlide % totalSlides]) {
        dots[currentSlide % totalSlides].classList.add("active");
    }
}

// Próximo slide
function nextSlide() {
    if (transitioning) return;

    const itemWidth = originals[0].offsetWidth + 25;
    currentSlide++;
    transitioning = true;

    track.style.transition = "transform 0.6s ease-in-out";
    track.style.transform = `translateX(-${currentSlide * itemWidth}px)`;

    if (currentSlide >= totalSlides) {
        // Após transição, volta para o início sem animação
        setTimeout(() => {
            track.style.transition = "none";
            currentSlide = 0;
            track.style.transform = `translateX(0)`;
            updateCarousel();
            transitioning = false;
        }, 650);
    } else {
        setTimeout(() => transitioning = false, 650);
        updateCarousel();
    }
}

// Auto-slide a cada 4 segundos
let autoSlide = setInterval(nextSlide, 4000);

// Reinicia o temporizador de auto-slide ao clicar em ponto
function resetAutoSlide() {
    clearInterval(autoSlide);
    autoSlide = setInterval(nextSlide, 4000);
}

// Atualiza o carrossel ao redimensionar a janela
window.addEventListener("resize", updateCarousel);

// Inicializa
updateCarousel();

// Pausar auto-slide ao passar o mouse sobre um item
const carrosselItems = track.querySelectorAll("a");

carrosselItems.forEach(item => {
  item.addEventListener("mouseenter", () => {
    clearInterval(autoSlide);
  });

  item.addEventListener("mouseleave", () => {
    resetAutoSlide();
  });
});