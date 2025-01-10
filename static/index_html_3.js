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
