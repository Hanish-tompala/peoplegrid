chrome.runtime.onInstalled.addListener(() => {
  chrome.scripting.registerContentScripts([{
    id: "god-mode-copy",
    matches: ["<all_urls>"],
    js: ["content.js"],
    runAt: "document_start",
    world: "MAIN", // <--- This is the key. Runs alongside the site's own JS.
    allFrames: true
  }]);
});