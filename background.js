console.log("Service worker started");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    
    // Get page data and save
    if(message.action === "getPageData") {
        chrome.tabs.sendMessage(
            message.tabId,
            {
                action: "getPageData"
            },
            async (response) => {
                console.log("Page data from content script:", response);
                try {
                    const apiResponse = await fetch(
                        "http://127.0.0.1:8000/bookmarks",
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(response)
                        }
                    );
                    const data = await apiResponse.json();
                    console.log("Response from FastAPI:", data);
                    sendResponse(data);
                } catch (error) {
                    console.error("Error sending data to FastAPI:", error);
                    sendResponse({ error: "Failed to send data to FastAPI" });
                }
            }
        );
        return true;
    }

    // Get all bookmarks
    if (message.action === "getBookmarks") {

            fetch(
                "http://127.0.0.1:8000/bookmarks"
            )
                .then((response) => response.json())
                .then((data) => {

                    console.log(
                        "Bookmarks from FastAPI:",
                        data
                    );

                    sendResponse(data);

                })
                .catch((error) => {

                    console.error(
                        "Error fetching bookmarks:",
                        error
                    );

                    sendResponse({
                        error: "Could not fetch bookmarks"
                    });
                });

            return true;
        }
    
    // Delete Bookmark
    if (message.action === "deleteBookmark") {
        fetch (
            `http://127.0.0.1:8000/bookmark/${message.bookmarkId}`,
            {
                method: "DELETE"
            }
        )
            .then((response) => response.json())
            .then((data) => {
                console.log("Delete response from FastAPI:", data);
                sendResponse(data);
            })
            .catch((error) => {
                console.log("Error deleting bookmark:", error);
                sendResponse({ error: "Failed to delete bookmark" });
            });
            return true;
        }

    // Search Bookmarks
    if (message.action === "searchBookmarks") {

        const query = encodeURIComponent(message.query);
        const url = `http://127.0.0.1:8000/bookmarks/search?query=${query}`;

        console.log("Search URL:", url);

        fetch(url)
            .then((response) => {

                console.log("Search HTTP status:", response.status);
                return response.json();
            })
            .then((data) => {

                console.log("Search results from FastAPI:", data);
                sendResponse(data);

            })
            .catch((error) => {

                console.error("Error searching bookmarks:", error);
                sendResponse({
                    error: "Could not search bookmarks"
                });
            });

        return true;
    }
});