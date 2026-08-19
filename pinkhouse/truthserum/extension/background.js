const DEFAULT_API = "http://127.0.0.1:8080";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "truthserum-selection",
    title: "Check with Truth Serum",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "truthserum-selection") return;
  const text = (info.selectionText || "").trim();
  if (!text) return;
  await chrome.storage.session.set({ pendingText: text, pendingResult: null });
  if (tab && tab.id) {
    try {
      await chrome.action.openPopup();
    } catch (_) {
      // openPopup may be unavailable; popup still reads session storage on open
    }
  }
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg?.type === "ANALYZE_TEXT") {
    analyze(msg.text)
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err.message || String(err) }));
    return true;
  }
  if (msg?.type === "GET_VISIBLE_TEXT") {
    return false;
  }
});

async function getApiBase() {
  const stored = await chrome.storage.sync.get({ apiBase: DEFAULT_API });
  return (stored.apiBase || DEFAULT_API).replace(/\/$/, "");
}

async function analyze(text) {
  const base = await getApiBase();
  const res = await fetch(`${base}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || data.error || `HTTP ${res.status}`);
  }
  return data;
}
