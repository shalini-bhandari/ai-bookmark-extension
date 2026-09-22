console.log("Service worker started");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.action === "getPageData") {
        chrome.tabs.sendMessage(
            message.tabId,
            {
                action: "getPageData"
            },
            (response) => {
                sendResponse(response);
            }
        );
        return true;
    }
})