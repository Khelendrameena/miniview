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
  
  function uploadImage() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = "image/*";
  input.onchange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const img = `<img src="${URL.createObjectURL(file)}" alt="Image" style="max-width:100%;margin:10px 0;border-radius:8px;"/>`;
      document.getElementById("editor").insertAdjacentHTML("beforeend", img);

      // Now send the image to the server via AJAX using FormData
      const formData = new FormData();
      formData.append("image", file);
      formData.append("csrfmiddlewaretoken", '{{ csrf_token }}');  // Add CSRF token if you're using Django
      
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/vlog/internal", true);
      xhr.onload = function() {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          const imageUrl = response.image_url;  // Assuming backend returns image URL
          // You can then replace the image source with the actual uploaded image URL
          const imgElement = document.querySelector("img[src='" + URL.createObjectURL(file) + "']");
          imgElement.src = imageUrl;
        } else {
          alert("Error uploading the image.");
        }
      };
      xhr.send(formData);
    }
  };
  input.click();
}
 // Function to upload a file
 function uploadFile() {
   const input = document.createElement("input");
   input.type = "file";
   input.accept = "application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/*";
   input.onchange = (event) => {
     const file = event.target.files[0];
     if (file) {
       // Handle file upload and preview
       handleFilePreview(file);
     }
   };
   input.click();
 }

 // Function to display file preview in the editor
 function handleFilePreview(file) {
   const fileName = file.name;
   const fileType = file.type;
   const fileUrl = URL.createObjectURL(file);

   let filePreviewHtml = '';

   // Check for file type and show appropriate preview
   if (fileType.startsWith('image/')) {
     filePreviewHtml = `<div class="file-preview">
                          <img src="${fileUrl}" alt="${fileName}" style="max-width: 100px; max-height: 100px; margin: 10px 0;"/>
                          <span>${fileName}</span>
                        </div>`;
   } else if (fileType === 'application/pdf') {
     // Generate thumbnail for PDF using PDF.js
     filePreviewHtml = `<div class="file-preview" id="pdf-preview-${fileName}">
                          <canvas id="canvas-${fileName}" style="max-width: 100px; max-height: 100px; margin: 10px 0;"></canvas>
                          <span>${fileName}</span>
                          <button onclick="viewFile('${fileUrl}')">View</button>
                        </div>`;
     generatePdfThumbnail(file, fileName);
   } else {
     filePreviewHtml = `<div class="file-preview">
                          <img src="file-icon.png" alt="File" style="max-width: 100px; margin: 10px 0;"/>
                          <span>${fileName}</span>
                        </div>`;
   }

   // Insert the preview HTML in the editor
   document.getElementById("editor").insertAdjacentHTML("beforeend", filePreviewHtml);
 }

 // Function to generate PDF thumbnail using PDF.js
 function generatePdfThumbnail(file, fileName) {
   const reader = new FileReader();
   reader.onload = function(e) {
     const loadingTask = pdfjsLib.getDocument(e.target.result);
     loadingTask.promise.then(function(pdf) {
       // Get the first page
       pdf.getPage(1).then(function(page) {
         const scale = 0.5;
         const viewport = page.getViewport({ scale: scale });

         const canvas = document.getElementById(`canvas-${fileName}`);
         const context = canvas.getContext("2d");

         // Set canvas dimensions
         canvas.width = viewport.width;
         canvas.height = viewport.height;

         // Render the page into the canvas
         page.render({
           canvasContext: context,
           viewport: viewport
         });
       });
     });
   };
   reader.readAsArrayBuffer(file);
 }

 // Function to view PDF (or other files) when clicked
 function viewFile(fileUrl) {
   // Open the file URL (e.g., open PDF in a new window)
   window.open(fileUrl, '_blank');
 }
