  // Format text using execCommand
  function formatText(command) {
    document.execCommand(command, false, null);
  }

  // Add heading
  function addHeading() {
    const text = prompt("Enter your heading text:");
    if (text) {
      const heading = `<h2>${text}</h2>`;
      document.getElementById("editor").insertAdjacentHTML("beforeend", heading);
    }
  }

  // Add text
  function addText() {
    const text = prompt("Enter your text:");
    if (text) {
      const paragraph = `<p>${text}</p>`;
      document.getElementById("editor").insertAdjacentHTML("beforeend", paragraph);
    }
  }

function addCode() {
  const code = prompt("Enter your code:");
  if (code) {
    const sanitizedCode = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const codeBlock = `<pre><code class="language-javascript">${sanitizedCode}</code></pre>`;
    document.getElementById("editor").insertAdjacentHTML("beforeend", codeBlock);

    // Reinitialize Prism to apply syntax highlighting after the new code block is added
    Prism.highlightAll();
  }
}

  // Submit code via AJAX
  function submitCode() {
    const editorContent = document.getElementById("editor").innerHTML.trim();

    if (!editorContent || editorContent === "Start creating your vlog here...") {
      alert("Please create some content before submitting!");
      return;
    }

    // Show the loader
    document.getElementById("loader").style.display = "block";

    // Create AJAX request
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/@${document.getElementById("username").innerText}/vlog/publish`, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    // Prepare the data
    const data = JSON.stringify({ content: editorContent });

    // Send the request
    xhr.send(data);

    // Handle the response
    xhr.onload = function() {
      // Hide the loader
      document.getElementById("loader").style.display = "none";

      if (xhr.status == 200) {
        // Show success message
        document.head.innerHTML = `  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: Arial, sans-serif;
      background-color: #f4f7fc;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }

    .container {
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .confirmation-box {
      background-color: white;
      border-radius: 8px;
      padding: 40px;
      text-align: center;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      max-width: 400px;
      width: 100%;
    }

    .checkmark {
      font-size: 50px;
      color: #4caf50;
    }

    h2 {
      margin: 20px 0;
      font-size: 24px;
      color: #333;
    }

    p {
      font-size: 16px;
      color: #555;
      margin-bottom: 20px;
    }

    button {
      padding: 10px 20px;
      background-color: #0078ff;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    button:hover {
      background-color: #005bb5;
    }
  </style>`;
            document.body.innerHTML = `
  <div class="container">
    <div class="confirmation-box">
      <div class="checkmark">
        ✔
      </div>
      <h2>Your Vlog was uploaded successfully!</h2>
      <p>Your vlog has been uploaded to the platform. You can now share it with your audience.</p>
      <button onclick="goToHomePage()">Go to Home</button>
    </div>
  </div>`;
      
      } else {
        alert("There was an error submitting your vlog.");
      }
    };

    xhr.onerror = function() {
      // Hide the loader
      document.getElementById("loader").style.display = "none";
      alert("Error submitting the vlog.");
    };
  }
  
  let uploadedImages = []; // Array to store files temporarily

function uploadImage() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Add the image to the temporary storage array
      uploadedImages.push(file);

      // Display the image preview
      const img = `<img src="${URL.createObjectURL(file)}" alt="Image" style="max-width:100%;margin:10px 0;border-radius:8px;"/>`;
      document.getElementById("editor").insertAdjacentHTML("beforeend", img);
    }
  };
  input.click();
}

function submitImages() {
  if (uploadedImages.length === 0) {
    alert("No images to upload.");
    return;
  }

  const formData = new FormData();
  uploadedImages.forEach((file, index) => {
    formData.append(`image_${index}`, file); // Append each file with a unique key
  });
  formData.append("csrfmiddlewaretoken", '{{ csrf_token }}'); // CSRF token for Django

  // AJAX request to upload the images
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/vlog/internal", true);
  xhr.onload = function () {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      alert("Images uploaded successfully!");
      console.log("Response:", response);
    } else {
      alert("Error uploading the images.");
    }
  };
  xhr.send(formData);

  // Clear the uploadedImages array and editor after successful upload
  uploadedImages = [];
  document.getElementById("editor").innerHTML = "";
}

 // Function to upload a file
 
