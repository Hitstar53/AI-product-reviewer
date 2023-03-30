const searchbtn = document.querySelector(".searchButton");
const modelans = document.querySelector(".model-answer");
const modelrev = document.querySelector(".model-review");

searchbtn.addEventListener("click", function () {
    modelans.style.display = "block";
    modelrev.innerHTML = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur ducimus aspernatur, fugiat labore aliquid assumenda. Suscipit delectus aliquid impedit reprehenderit. Saepe ea, nostrum facilis maxime dolores eum voluptatem nisi veritatis doloremque eaque inventore ipsam voluptatum cum.";
});
