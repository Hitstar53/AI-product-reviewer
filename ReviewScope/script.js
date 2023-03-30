const searchbtn = document.querySelector(".searchButton");
const modelans = document.querySelector(".model-answer");
const modelrate = document.querySelector(".model-rating");
const modelrev = document.querySelector(".model-review");
const loader = document.querySelector(".loader");

searchbtn.addEventListener("click", function () {
    modelans.style.display = "block";
    //display loader for 3 seconds
    setTimeout(function () {
        loader.style.display = "none";
        modelrate.style.display = "block";
    }, 3000);
    modelrev.innerHTML = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur ducimus aspernatur, fugiat labore aliquid assumenda. Suscipit delectus aliquid impedit reprehenderit. Saepe ea, nostrum facilis maxime dolores eum voluptatem nisi veritatis doloremque eaque inventore ipsam voluptatum cum.";
});
