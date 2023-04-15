const searchbtn = document.querySelector(".searchButton");
const modelans = document.querySelector(".model-answer");
const modelrate = document.querySelector(".model-rating");
const modelrev = document.querySelector(".model-review");
const loader = document.querySelector(".loader");
const stars = document.querySelectorAll(".star");
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
    }, 2000);
    let random = Math.floor(Math.random() * 6) + 1;
    for (let i=4;i>=random;i--) {
        stars[i].style.fill = "#444654"
    }
    for (let i=0;i<random-1;i++) {
        stars[i].style.fill = "#ffd700"
    }
    modelrev.innerHTML = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur ducimus aspernatur, fugiat labore aliquid assumenda. Suscipit delectus aliquid impedit reprehenderit. Saepe ea, nostrum facilis maxime dolores eum voluptatem nisi veritatis doloremque eaque inventore ipsam voluptatum cum.";
});

// Capture the input URL from your Chrome extension
// Get the form element and add an event listener for form submission
// var inputUrl = "https://www.amazon.in/Redmi-Storage-Super-Amoled-Display/product-reviews/B0948NNY3W/ref=cm_cr_dp_d_s";
var searchForm = document.getElementById('searchForm');
var inputValue = '';
searchForm.addEventListener('submit', function (event) {
    event.preventDefault();
    // Get the input text value from the input element
    var searchInput = document.getElementById('query');
    var inputValue = searchInput.value;
    console.log('Input value:', inputValue);
    var inputUrl = inputValue;
    // Send an HTTP POST request to your Django REST API endpoint
    fetch('http://127.0.0.1:8000/api/review/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({product_url: inputUrl}),
    })
    .then(response => {
        // Handle the response from the Django REST API
        if (response.ok) {
            // Success
            console.log('URL sent to Django API successfully');
            // get the response data
            console.log(response.json());
        } else {
            // Error
            console.error('Failed to send URL to Django API:', response.statusText);
        }
    })
    .catch(error => {
        // Handle any errors that may occur during the HTTP request
        console.error('Error sending URL to Django API:', error);
    });
});
