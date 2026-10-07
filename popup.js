// get page data button
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

// View bookmarks button
const bookmarksButton = document.getElementById("getBookmarks");
const bookmarksContainer = document.getElementById("bookmarks");

bookmarksButton.addEventListener("click", loadBookmarks);

// Function to load bookmarks and display them in the popup
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

// Function to display a bookmark in the popup
function displayBookmark(bookmark, container) {
    const bookmarkElement = document.createElement("div");
    const title = document.createElement("h3");
    title.textContent = bookmark.title;

    const url = document.createElement("p");
    url.textContent = bookmark.url;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";

    deleteButton.addEventListener("click", () => {
        deleteBookmark(bookmark._id);
    });

    bookmarkElement.appendChild(title);
    bookmarkElement.appendChild(url);
    bookmarkElement.appendChild(deleteButton);

    container.appendChild(bookmarkElement);
}

// Function to delete a bookmark
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

// Search bookmarks button
const searchButton = document.getElementById("searchButton");
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");
const semanticSearchButton = document.getElementById("semanticSearchButton");
const askInput = document.getElementById("askInput")
const askButton = document.getElementById("askButton");
const askAnswer = document.getElementById("askAnswer");
const askSources = document.getElementById("askSources");

searchButton.addEventListener("click", searchBookmarks);
semanticSearchButton.addEventListener("click", semanticSearchBookmarks);
askButton.addEventListener("click", askAI);

// Search function
function searchBookmarks() {
    const query = searchInput.value.trim();
    if (!query) {
        searchResults.textContent = "Please enter a search query.";
        return;
    }
    console.log("Searching bookmarks for:", query);

    chrome.runtime.sendMessage(
        {
            action: "searchBookmarks",
            query: query
        },
        (response) => {
            console.log("Search results:", response);
            searchResults.innerHTML = "";

            if (!response || response.error) {
                searchResults.textContent = "Error occurred while searching.";
                return;
            }
            if (response.bookmarks.length === 0) {
                searchResults.textContent = "No bookmarks found.";
                return;
            }

            response.bookmarks.forEach((bookmark) => {
                displayBookmark(bookmark, searchResults);
            });
        }
    );
}

function semanticSearchBookmarks() {
    const query = searchInput.value.trim();

    if(!query) {
        searchResults.textContent = "Please eneter a search query.";
        return;
    }

    console.log("AI searching for:", query);

    chrome.runtime.sendMessage(
        {
            action: "semanticSearchBookmarks",
            query: query
        },
        (response) => {
            console.log("Semantic search response:", response);
            searchResults.innerHTML = "";
            
            if(!response || response.error) {
                searchResults.textContent = "Error occurred while searching.";
                return;
            }

            if(!Array.isArray(response.bookmarks)){
                console.error("Unexpected response:", response);
                searchResults.textContent = "Unexpected response from server.";
                return;
            }

            if(response.bookmarks.length === 0) {
                searchResults.textContent = "No bookmarks found.";
                return;
            }
            response.bookmarks.forEach((bookmark) => {
                displaySemanticBookmark(bookmark, searchResults);
            });
        }
    );
}

function displaySemanticBookmark(bookmark, container) {
    const bookmarkElement = document.createElement("div");

    const title = document.createElement("h3");
    title.textContent = bookmark.title;
    
    const url = document.createElement("p");
    url.textContent = bookmark.url;

    const chunk = document.createElement("p");
    chunk.textContent = bookmark.content;

    const score = document.createElement("p");
    score.textContent = "Similarity Score: " + bookmark.similarity_score.toFixed(4);

    bookmarkElement.appendChild(title);
    bookmarkElement.appendChild(url);
    bookmarkElement.appendChild(chunk);
    bookmarkElement.appendChild(score);

    container.appendChild(bookmarkElement);
}

function askAI() {
    const question = askInput.value.trim();

    if(!question) {
        askAnswer.textContent = "Please enter a question";
        askSources.innerHTML = "";
        return
    }

    askAnswer.textContent = "Thinking...";
    askSources.innerHTML = "";

    chrome.runtime.sendMessage(
        {
            action: "askAI",
            question: question
        },
        (response) => {

            console.log("AI answer:", response);

            if (!response || response.error) {
                askAnswer.textContent =
                    "Error while getting AI answer.";
                return;
            }

            askAnswer.textContent = response.answer;
            askSources.innerHTML = "";

            if (Array.isArray(response.sources) && response.sources.length > 0) {
                const heading = document.createElement("h3");
                heading.textContent = "Sources";
                askSources.appendChild(heading);

                response.sources.forEach((source) => {

                    const sourceElement = document.createElement("div");
                    const title = document.createElement("button");
                    title.textContent = "Open: " + source.title;

                    title.style.display = "block";
                    title.style.marginBottom = "8px";
                    title.style.cursor = "pointer";
                    title.style.width = "100%";
                    title.style.boxSizing = "border-box";

                    title.addEventListener("click", () => {
                        chrome.tabs.create({
                            url: source.url
                        });
                    });
                    const metadata = document.createElement("p");
                    metadata.textContent =
                        `Chunk ${source.chunk_index} | ` +
                        `Similarity: ${source.similarity_score.toFixed(4)}`;

                    const content = document.createElement("p");
                    content.textContent = `"${source.chunk_content}"`;
                    
                    sourceElement.appendChild(title);
                    sourceElement.appendChild(metadata);
                    sourceElement.appendChild(content);

                    askSources.appendChild(sourceElement);
                });
            }
        }
    );
}