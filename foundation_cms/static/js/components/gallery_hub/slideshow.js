const SELECTORS = {
  root: "[data-gallery-hub-slideshow]",
  slide: "[data-gallery-hub-slide]",
  previous: "[data-gallery-hub-slide-previous]",
  next: "[data-gallery-hub-slide-next]",
  dots: "[data-gallery-hub-slide-dots]",
};

const CLASSES = {
  active: "is-active",
  afterActive: "is-after-active",
  beforeActive: "is-before-active",
  leavingNext: "is-leaving-next",
  restoringPrevious: "is-restoring-previous",
};

const ANIMATION_DURATION = 560;
const SLIDE_EASING = "cubic-bezier(0.22, 1, 0.36, 1)";
const MAX_DOTS = 3;

function setVideoPlayback(slide, shouldPlay) {
  slide.querySelectorAll("video").forEach((video) => {
    if (shouldPlay) {
      video.play().catch(() => {});
      return;
    }

    video.pause();
  });
}

function createDot(index) {
  const dot = document.createElement("button");

  dot.className = "gallery-hub-project__slide-dot";
  dot.type = "button";
  dot.dataset.galleryHubSlideDot = `${index}`;
  dot.setAttribute("aria-label", `View media ${index + 1}`);

  return dot;
}

function initSlideshow(root) {
  const slides = Array.from(root.querySelectorAll(SELECTORS.slide));
  const previous = root.querySelector(SELECTORS.previous);
  const next = root.querySelector(SELECTORS.next);
  const dotsContainer = root.querySelector(SELECTORS.dots);
  const dots = [];
  let activeIndex = 0;
  let animationTimeout = null;
  let activeAnimation = null;

  if (slides.length <= 1) {
    previous.hidden = true;
    next.hidden = true;
    dotsContainer.hidden = true;
    return;
  }

  Array.from({ length: Math.min(slides.length, MAX_DOTS) }).forEach((_, index) => {
    const dot = createDot(index);

    dot.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      goToSlide(Number(dot.dataset.galleryHubSlideDot));
    });

    dots.push(dot);
    dotsContainer.append(dot);
  });

  function syncControls() {
    previous.disabled = activeIndex === 0;
    next.disabled = activeIndex === slides.length - 1;

    const dotStart = Math.min(
      Math.max(activeIndex - 1, 0),
      Math.max(slides.length - dots.length, 0),
    );

    dots.forEach((dot, index) => {
      const slideIndex = dotStart + index;
      const isActive = slideIndex === activeIndex;

      dot.dataset.galleryHubSlideDot = `${slideIndex}`;
      dot.setAttribute("aria-label", `View media ${slideIndex + 1}`);
      dot.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  function syncSlides() {
    slides.forEach((slide, index) => {
      const isActive = index === activeIndex;

      slide.classList.toggle(CLASSES.active, isActive);
      slide.classList.toggle(CLASSES.beforeActive, index < activeIndex);
      slide.classList.toggle(CLASSES.afterActive, index > activeIndex);
      slide.setAttribute("aria-hidden", `${!isActive}`);
      slide.style.zIndex = `${slides.length - Math.abs(index - activeIndex)}`;
      setVideoPlayback(slide, isActive);
    });

    syncControls();
  }

  function goToSlide(index) {
    if (index === activeIndex || index < 0 || index >= slides.length) return;

    const previousIndex = activeIndex;
    const currentSlide = slides[previousIndex];
    const targetSlide = slides[index];
    const direction = index > previousIndex ? 1 : -1;

    window.clearTimeout(animationTimeout);
    activeAnimation?.cancel();
    slides.forEach((slide) => {
      slide.classList.remove(CLASSES.leavingNext, CLASSES.restoringPrevious);
    });

    if (direction < 0) {
      targetSlide.classList.add(CLASSES.restoringPrevious);
    }

    activeIndex = index;
    syncSlides();

    if (direction > 0) {
      currentSlide.classList.add(CLASSES.leavingNext);
      currentSlide.style.zIndex = `${slides.length + 2}`;
    } else {
      targetSlide.style.zIndex = `${slides.length + 2}`;
      activeAnimation = targetSlide.animate(
        [
          {
            opacity: 0,
            transform: "translateX(32%) rotate(2deg)",
          },
          {
            opacity: 1,
            transform: "translateX(0) rotate(0deg)",
          },
        ],
        {
          duration: ANIMATION_DURATION,
          easing: SLIDE_EASING,
        },
      );
      activeAnimation.addEventListener("finish", () => {
        activeAnimation = null;
      });
    }

    animationTimeout = window.setTimeout(() => {
      currentSlide.classList.remove(CLASSES.leavingNext);
      targetSlide.classList.remove(CLASSES.restoringPrevious);
      activeAnimation = null;
      syncSlides();
    }, ANIMATION_DURATION);
  }

  previous.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    goToSlide(activeIndex - 1);
  });

  next.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    goToSlide(activeIndex + 1);
  });

  syncSlides();
}

export function initGalleryHubSlideshows() {
  document.querySelectorAll(SELECTORS.root).forEach(initSlideshow);
}
