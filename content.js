console.log("Content script loaded!");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getPageData") {

        const pageData = {
            title: document.title,
            url: window.location.href,
            content: document.body.innerText
        };

        sendResponse(pageData);
    }
});