document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const source = document.getElementById("source");
  const destination = document.getElementById("destination");
  const button = form.querySelector("button");

  form.addEventListener("submit", function (e) {
      if (source.value === destination.value) {
          e.preventDefault();
          alert("Source and destination cannot be the same.");
          return;
      }

      button.innerText = "Finding...";
      button.disabled = true;

      // Reset button after 1.5s to simulate backend processing
      setTimeout(() => {
          button.innerText = "Find Route";
          button.disabled = false;
      }, 1500);
  });
});
