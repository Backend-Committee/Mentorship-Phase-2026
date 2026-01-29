const header = document.querySelector("#main-header");

window.addEventListener("scroll", () => {
  if (window.scrollY > 100) {
    header.classList.add("hidden");
  } else {
    header.classList.remove("hidden");
  }
});

document.addEventListener("mousemove", (e) => {
  if (e.clientY < 20) {
    header.classList.remove("hidden");
  }
});
