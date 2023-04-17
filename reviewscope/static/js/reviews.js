reviews = document.querySelectorAll('.card');
var i = 1;
// iterate through each review
reviews.forEach((review) => {
    if(i == 1)
        review.style.backgroundColor = '#3fbafe';
    else if(i == 2)
        review.style.backgroundColor = '#f7a976';
    else if(i == 3)
        review.style.backgroundColor = '#b69efe';
    else if(i == 4)
        review.style.backgroundColor = '#60efbc';
    else if(i == 5)
        review.style.backgroundColor = '#f588d8';
    else
        i = 1;
    i++;
});

function myFunction() {
    // Declare variables
    var input, filter, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    reviews = document.querySelectorAll('.card');
    // Loop through all list items, and hide those who don't match the search query
    reviews.forEach((review) => {
        txtValue = review.textContent || review.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            review.style.display = "";
        } else {
            review.style.display = "none";
        }
    });
}

// charts.js
const ctx1 = document.getElementById('myChart1');
const ctx2 = document.getElementById('myChart2');
const ctx3 = document.getElementById('myChart3');

const myChart = new Chart(ctx1, {
    type: 'doughnut',
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(0, 255, 0, 0.2)',
                'rgba(255, 0, 0, 0.2)',
                'rgba(0, 0, 255, 0.2)'
            ],
            borderColor: [
                'rgba(0, 255, 0, 1)',
                'rgba(255, 0, 0, 1)',
                'rgba(0, 0, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const myChart2 = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3],
            backgroundColor: [
                'rgba(0, 255, 0, 0.2)',
                'rgba(255, 0, 0, 0.2)',
                'rgba(0, 0, 255, 0.2)'
            ],
            borderColor: [
                'rgba(0, 255, 0, 1)',
                'rgba(255, 0, 0, 1)',
                'rgba(0, 0, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});