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
