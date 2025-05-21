let carToDelete = null;

function confirmDelete(carId) {
  carToDelete = carId;
  document.getElementById("delete-modal").classList.remove("hidden");
  document.body.classList.add("overflow-hidden");
}

function closeDeleteModal() {
  carToDelete = null;
  document.getElementById("delete-modal").classList.add("hidden");
  document.body.classList.remove("overflow-hidden");
}

document.body.addEventListener("click", function (event) {
  if (event.target && event.target.id === "confirm-delete-btn") {
    // Get the carId from the button or another place
    if (carToDelete) {
      fetch(`/cars/${carToDelete}/delete/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: new URLSearchParams({
          car_id: carToDelete,
        }),
      })
        .then((response) => {
          if (response.ok) {
            document.getElementById(`car-${carToDelete}`).remove();
            closeDeleteModal();
            alert("Car deleted successfully!");
          } else {
            alert("Failed to delete car. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred. Please try again.");
        });
    }
  }
});

// Helper function to get the CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
