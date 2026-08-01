(() => {
  const nav = document.querySelector("[data-nav]");
  const toggle = document.querySelector("[data-nav-toggle]");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.18 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  const main = document.querySelector("[data-main-image]");
  const thumbs = document.querySelectorAll("[data-thumb]");
  if (main && thumbs.length) {
    thumbs.forEach((btn) => {
      btn.addEventListener("click", () => {
        const src = btn.getAttribute("data-thumb");
        if (!src) return;
        main.setAttribute("src", src);
        thumbs.forEach((t) => t.setAttribute("aria-current", "false"));
        btn.setAttribute("aria-current", "true");
      });
    });
  }
})();
