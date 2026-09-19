const button = document.getElementById('helloButton');

button.addEventListener("click", function () {
    document.getElementById("message").textContent = "Hello from my Chrome Extension !";
});