document.addEventListener("DOMContentLoaded", function () {
  const favButton = document.getElementById("favourite-btn");
  if (favButton) {
    favButton.addEventListener("click", function () {
      const materialId = this.getAttribute("data-material-id");
      const csrfToken = document.getElementById("csrf_token").value;

      fetch(`/materials/${materialId}/favourite/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-type": "application/json",
        },
        credentials: "same-origin",
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "added") {
            favButton.textContent = "Remove Favourite";
          } else if (data.status === "removed") {
            favButton.textContent = "Add Favourite";
          }
        })
        .catch((error) => console.error("Error: " + error));
    });
  }
});

