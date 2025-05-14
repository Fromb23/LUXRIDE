
  // Define functions first
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function updateStatus(selectElement, recordId) {
    console.log('Updating status for record ID:', recordId);
    const selectedStatus = selectElement.value;
    const url = `/update-borrowed-car-status/${recordId}/`;
    const csrftoken = getCookie('csrftoken');

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        status: selectedStatus,
        record_id: recordId
      })
    })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        if (data.success) {
          alert('Status updated successfully');
          selectElement.dataset.previousValue = selectedStatus;
          console.error('Error updating status:', data.error);
          selectElement.value = selectElement.dataset.previousValue;
        }
      })
      .catch(error => {
        console.error('Error:', error);
        selectElement.value = selectElement.dataset.previousValue;
      });
  }

  // Initialize on DOM load
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[id^="status-dropdown-"]').forEach(select => {
      select.dataset.previousValue = select.value;
    });
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
  });