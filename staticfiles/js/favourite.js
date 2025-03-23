document.addEventListener("DOMContentLoaded", function () {
  const favButton = document.getElementById("favourite-btn");

  if (favButton) {
    favButton.addEventListener("click", function () {
      const materialId = this.getAttribute("data-material-id");
      const csrfToken = getCookie("csrftoken");

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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
