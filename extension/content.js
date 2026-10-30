// Content script injected into YouTube Studio & YouTube
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "GET_YOUTUBE_TITLE") {
    // 1. YouTube Studio Upload / Details Modal
    const studioTitle = document.querySelector("#textbox[contenteditable='true']") ||
                        document.querySelector("input[aria-label*='Title']");
    if (studioTitle) {
      const val = studioTitle.innerText || studioTitle.value || "";
      sendResponse({ title: val.trim() });
      return true;
    }

    // 2. Standard YouTube Watch Page (if testing on live video)
    const watchTitle = document.querySelector("h1.ytd-watch-metadata yt-formatted-string") ||
                       document.querySelector("h1.title");
    if (watchTitle) {
      sendResponse({ title: (watchTitle.innerText || "").trim() });
      return true;
    }

    sendResponse({ title: "" });
  }
  return true;
});
