    const followButton = document.getElementById("follow_button_2");

    function follow_8() {
      if (followButton.innerText === "Follow") {
        data_8(document.getElementById("follow_id").innerText, 1); // Pass profile ID
        followButton.innerText = "Followed";
      } else {
        data_8(document.getElementById("follow_id").innerText, -1); // Pass profile ID
        followButton.innerText = "Follow";
      }
    }

    function data_8(id, follow) {
      var xhr = new XMLHttpRequest();
      var path = document.getElementById("name_profile").innerText;
      xhr.open('POST', `/app/${path}/follow`, true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
      xhr.send(JSON.stringify({ "id": id, "follow": follow }));

      // Handle the response from the server
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          if (xhr.status === 200) {
            try {
              const response = JSON.parse(xhr.responseText);
              if (response.success) {                                                                                                                                   console.log(response.message); // Success message
              } else {
                alert(response.error || "An error occurred.");
              }
            } catch (error) {
              console.error("something wrong");
            }
          } else {
          alert("something wrong");
          }
        }
      };
    }

    // Show the modal for unauthenticated users
    function showCustomAlert() {
      const modal = document.getElementById('customAlert');
      modal.style.display = 'flex'; // Show modal
      document.body.classList.add('modal-active'); // Disable page scroll
    }

    // Close the modal
    function closeCustomAlert() {
      const modal = document.getElementById('customAlert');
      modal.style.display = 'none'; // Hide modal
      document.body.classList.remove('modal-active'); // Enable page scroll
    }
  
