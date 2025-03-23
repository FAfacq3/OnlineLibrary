document.addEventListener("DOMContentLoaded", function () {
  const reviewForm = document.getElementById("review-form");
  if (reviewForm) {
    reviewForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(reviewForm);
      const materialId = reviewForm.getAttribute("data-material-id");
      const csrfToken = reviewForm.querySelector(
        '[name="csrfmiddlewaretoken"]'
      ).value;

      fetch(`/materials/${materialId}/review/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const reviewSection = document.getElementById("review-section");
            const newReview = document.createElement("div");
            newReview.classList.add("border-bottom", "pb-2", "mb-2");
            newReview.innerHTML = `
                    <p><strong>${data.username}</strong> rated: ${data.rating}/5</p>
                    <p>${data.comment}</p>
                    <p class="text-muted small">${data.created_at}</p>
                `;

            reviewSection.prepend(newReview);
            reviewForm.reset();
          } else {
            alert("Error submitting review. Please try again.");
          }
        })
        .catch((error) => console.error("Error: ", error));
    });
  }
});
