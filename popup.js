const button = document.getElementById("getPageData");
const pageTitle = document.getElementById("pageTitle");

button.addEventListener("click", async () => {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    chrome.tabs.sendMessage(
        tab.id,
        {
            action: "getPageData"
        },
        (response) => {
            console.log("Page data received:", response);
            pageTitle.textContent = response.title;
        }
    );
});