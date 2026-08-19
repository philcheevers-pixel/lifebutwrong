chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg?.type === "GET_SELECTION") {
    sendResponse({ text: (window.getSelection() || "").toString() });
    return true;
  }
  if (msg?.type === "GET_VISIBLE_TEXT") {
    const text = document.body ? document.body.innerText : "";
    sendResponse({ text: text.slice(0, 50000) });
    return true;
  }
});
