const searchbtn = document.querySelector(".searchButton");
const modelans = document.querySelector(".model-answer");
const modelrate = document.querySelector(".model-rating");
const modelrev = document.querySelector(".model-review");
const loader = document.querySelector(".loader");
const stars = document.querySelectorAll(".star");
const ratingp = document.querySelector(".rating");

// Capture the input URL from your Chrome extension
// Get the form element and add an event listener for form submission
// var inputUrl = "https://www.amazon.in/Redmi-Storage-Super-Amoled-Display/product-reviews/B0948NNY3W/ref=cm_cr_dp_d_s";

var searchForm = document.getElementById('searchForm');
var inputValue = '';
var summary = '';
var rating = 0;
searchForm.addEventListener('submit', function (event) {
    event.preventDefault();
    // Get the input text value from the input element
    var searchInput = document.getElementById('query');
    var inputValue = searchInput.value;
    console.log('Input value:', inputValue);
    var inputUrl = inputValue;
    // Send an HTTP POST request to your Django REST API endpoint
    fetch('https://ai-product-reviewer-production.up.railway.app/api/review/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({product_url: inputUrl}),
    })
    .then(response => {
        // Handle the response from the Django REST API
        if (response.ok) {
            console.log('URL sent to Django API successfully');
            response.json().then(data => {
                console.log('Django API response:', data);
                var summary = data[0].summary;
                var rating = data[0].rating;
                modelrev.innerHTML = summary;
                ratingp.innerHTML = "Rating by AI: "+rating+"/5";
                loader.style.display="None";
                modelrate.style.display="block";
                toggle = false;
                for (let i = 4; i >=parseInt(rating); i--) {
                    stars[i].style.fill = "#666874"
                }
                for(let i = 0; i < parseInt(rating) - 1; i++) {
                    stars[i].style.fill = "#ffd700"
                }
            });
        } else {
            console.error('Failed to send URL to Django API:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error sending URL to Django API:', error);
    });
});

let toggle = true;
searchbtn.addEventListener("click", function () {
    modelans.style.display = "block";
    if (!toggle) {
        loader.style.display = "block";
        modelrate.style.display = "none";
        toggle = true;
    }
    //display loader for 3 seconds
    setTimeout(function () {
        loader.style.display = "none";
        modelrate.style.display = "block";
        toggle = false;
    }, 99999);
});