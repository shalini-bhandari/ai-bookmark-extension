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

const bookmarksButton = document.getElementById("getBookmarks");
const bookmarksContainer = document.getElementById("bookmarks");

bookmarksButton.addEventListener("click", () => {

    chrome.runtime.sendMessage(
        {
            action: "getBookmarks"
        },
        (response) => {

            console.log("Bookmarks received:", response);

            bookmarksContainer.innerHTML = "";

            if (!response || !response.bookmarks) {
                bookmarksContainer.textContent =
                    "Could not load bookmarks.";
                return;
            }

            response.bookmarks.forEach((bookmark) => {

                const bookmarkElement = document.createElement("div");

                bookmarkElement.innerHTML = `
                    <h3>${bookmark.title}</h3>
                    <p>${bookmark.url}</p>
                `;

                bookmarksContainer.appendChild(bookmarkElement);
            });
        }
    );
});