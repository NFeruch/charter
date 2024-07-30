chrome.action.onClicked.addListener((tab) => {
    chrome.tabs.update(tab.id, {url: "http://localhost:8000/authorize"});
});