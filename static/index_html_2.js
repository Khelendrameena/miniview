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
  </script>
  <script>
if(window.innerWidth <= 500){
      document.getElementById("active_8").style.display = 'none';
  }
  else{
    document.getElementById("active_4").style.display = 'none';
  }

    function data(id, a, b, path) {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', path, true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
      xhr.send(JSON.stringify({ "id": id, "status": [a, b] }))
    }
    document.querySelectorAll('.like').forEach((app) => {
      app.addEventListener('click', (event) => {
        event.stopPropagation();
      })
    })

    document.querySelectorAll('.like_2').forEach((app) => {
      app.addEventListener('click', (event) => {
        event.stopPropagation();
      })
    })

    const spans = document.querySelectorAll('.flex.items-center.flex-wrap');
    spans.forEach((span) => {
      span.addEventListener('click', function() {
        document.querySelectorAll('.coment_22').forEach((com_22) => {
          com_22.addEventListener('click', () => {
            com_22.submit();

          })
        })
      });
    })


    function main_1(id) {
        data(id, 1, 0, '/view')
    }

    document.querySelectorAll('.like').forEach((like, index) => {
      like.addEventListener('click', () => {
        if (like.src == 'https://i.ibb.co/V3N06yK/icons8-heart-50-1.png') {
          
          like.src = 'https://i.ibb.co/FK8njDD/icons8-heart-50.png'
          data(`${document.querySelectorAll(".uid")[index].innerText}`, 0, -1, '/view')
          document.querySelectorAll(".like_2")[index].innerText--;
        }
        else {
          like.src = 'https://i.ibb.co/V3N06yK/icons8-heart-50-1.png'
          data(`${document.querySelectorAll(".uid")[index].innerText}`, 0, 1, '/view')
         document.querySelectorAll(".like_2")[index].innerText++;
        }
      })
    })
    if (window.innerWidth >= 480) {
      document.querySelectorAll('.p-4.md\\:w-1\\/3').forEach((div_4) => {
        div_4.className = 'lg:w-1/2 w-full mb-6 lg:mb-0';
      })
    }
