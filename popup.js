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
                if(response.error) {
                    pageTitle.textContent = response.error;
                    return;
                }
                pageTitle.textContent = response.message;
            }
        }
    );
});

const bookmarksButton = document.getElementById("getBookmarks");
const bookmarksContainer = document.getElementById("bookmarks");

bookmarksButton.addEventListener("click", loadBookmarks);

function loadBookmarks() {
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

                const title = document.createElement("h3");
                title.textContent = bookmark.title;

                const url = document.createElement("p");
                url.textContent = bookmark.url;

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "Delete";

                deleteButton.addEventListener(
                    "click",
                    () => {

                        deleteBookmark(bookmark._id);
                    }
                );


                bookmarkElement.appendChild(title);
                bookmarkElement.appendChild(url);
                bookmarkElement.appendChild(deleteButton);


                bookmarksContainer.appendChild(
                    bookmarkElement
                );
            });
        }
    );
}

function deleteBookmark(bookmark_id) {
    console.log("Deleting bookmark", bookmark_id);
    chrome.runtime.sendMessage(
        {
            action: "deleteBookmark",
            bookmarkId: bookmark_id
        },
        (response) => {
            console.log("Delete response:", response);
            if (response && !response.error) {
                loadBookmarks();
            }
            else {
                console.error(
                    "Error deleting bookmark:",
                    response.error
                );
            }
        }
    );
}