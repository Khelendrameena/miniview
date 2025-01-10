document.addEventListener('DOMContentLoaded', () => {
    let currentPage = 1; // शुरुआत में पेज 1 सेट करें
    let lastObservedDiv = null; // पहले से observe किए गए डिव को ट्रैक करें

    // Observer सेट करें
    const observer = new IntersectionObserver(async (entries, observerInstance) => {
        const lastEntry = entries[0];

        if (lastEntry.isIntersecting) {
            // पिछले div को unobserve करें
            if (lastObservedDiv) {
                observerInstance.unobserve(lastObservedDiv);
            }

            // जब यूजर पेज के अंत तक पहुंचे
            try {
                // लोडर दिखाएं
                showLoader();
                // Check if the current path is /search
             path = "{{ path }}"
                const response = await fetch(path, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: JSON.stringify({ currentPage: currentPage }),
                });

                const data = await response.json();

                if (data.html) {
                    const articlesContainer = document.getElementById('articles-container');
                    articlesContainer.insertAdjacentHTML('beforeend', data.html);
                    if (window.innerWidth >= 480) {
      document.querySelectorAll('.p-4.md\\:w-1\\/3').forEach((div_4) => {
        div_4.className = 'lg:w-1/2 w-full mb-6 lg:mb-0';
      })
    }
                    // पेज नंबर बढ़ाएं
                    currentPage++;

                    // DOM में नए ब्लॉग्स लोड होने के बाद lastDiv को अपडेट करें
                    observeLastDiv(observerInstance);
                } else {
                    console.error('No HTML data received');
                }
            } catch (error) {
                console.error('Error loading articles:', error);
            } finally {
                // लोडर को छुपाएं
                hideLoader();
            }
        }
    });

    // CSRF Token प्राप्त करने का फंक्शन
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // lastDiv को observe करने का फंक्शन
    function observeLastDiv(observerInstance) {
        const lastDiv = document.querySelectorAll('.coment');
        const loadMoreTarget = lastDiv[lastDiv.length - 1]; // सबसे आखिरी डिव को observe करें
        if (loadMoreTarget) {
            observerInstance.observe(loadMoreTarget); // Observer को फिर से नए lastDiv पर लागू करें
            lastObservedDiv = loadMoreTarget; // नए lastDiv को ट्रैक करें
        } else {
            console.error("Element with the required class not found.");
        }
    }

    // पहली बार observer शुरू करने के लिए lastDiv को observe करें
    observeLastDiv(observer);

    // लोडर दिखाने का फंक्शन
    function showLoader() {
        document.getElementById('loader').style.display = 'block';
    }

    // लोडर छुपाने का फंक्शन
    function hideLoader() {
        document.getElementById('loader').style.display = 'none';
    }
});
