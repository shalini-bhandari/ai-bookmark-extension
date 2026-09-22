const button = document.getElementById("getPageData");
const pageTitle = document.getElementById("pageTitle");

button.addEventListener("click", async () => {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    chrome.runtime.sendMessage(
        {
            action: "getPageData",
            tabId: tab.id
        },
        (response) => {
            console.log("Page data received:", response);
            if(response) {
                pageTitle.textContent = response.title;
            }
        }
    );
});