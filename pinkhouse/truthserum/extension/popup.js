const textEl = document.getElementById("text");
const errorEl = document.getElementById("error");
const out = document.getElementById("out");
const apiEl = document.getElementById("api");
let last = null;

const LABELS = {
  supported: "Supported",
  unsupported: "Unsupported / weakly supported",
  unclear: "Unclear / needs more context",
  conflation: "Possible conflation or leap",
};

chrome.storage.sync.get({ apiBase: "http://127.0.0.1:8080", kofiUrl: "https://ko-fi.com/" }, (cfg) => {
  apiEl.value = cfg.apiBase;
  document.getElementById("kofi").href = cfg.kofiUrl || "https://ko-fi.com/";
});

apiEl.addEventListener("change", () => {
  chrome.storage.sync.set({ apiBase: apiEl.value.trim().replace(/\/$/, "") });
});

chrome.storage.session.get({ pendingText: "" }, (data) => {
  if (data.pendingText) textEl.value = data.pendingText;
});

function showError(msg) {
  errorEl.hidden = !msg;
  errorEl.textContent = msg || "";
}

async function activeTab() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  return tabs[0];
}

document.getElementById("selection").addEventListener("click", async () => {
  showError("");
  const tab = await activeTab();
  if (!tab?.id) return;
  chrome.tabs.sendMessage(tab.id, { type: "GET_SELECTION" }, (res) => {
    if (chrome.runtime.lastError) {
      showError("Could not read selection on this page.");
      return;
    }
    textEl.value = (res && res.text) || "";
  });
});

document.getElementById("page").addEventListener("click", async () => {
  showError("");
  const tab = await activeTab();
  if (!tab?.id) return;
  chrome.tabs.sendMessage(tab.id, { type: "GET_VISIBLE_TEXT" }, (res) => {
    if (chrome.runtime.lastError) {
      showError("Could not read page text.");
      return;
    }
    const t = (res && res.text) || "";
    // Keep extension payloads modest
    textEl.value = t.split(/\s+/).slice(0, 2500).join(" ");
  });
});

document.getElementById("run").addEventListener("click", () => {
  showError("");
  const text = textEl.value.trim();
  if (words(text) < 10) {
    showError("Need a longer selection (at least a few sentences).");
    return;
  }
  if (words(text) > 3000) {
    showError("Selection too long for MVP (max ~3,000 words).");
    return;
  }
  chrome.runtime.sendMessage({ type: "ANALYZE_TEXT", text }, (res) => {
    if (!res?.ok) {
      showError(res?.error || "Analyze failed");
      return;
    }
    render(res.data);
  });
});

function words(t) {
  t = t.trim();
  return t ? t.split(/\s+/).length : 0;
}

function render(data) {
  last = data;
  out.hidden = false;
  const light = document.getElementById("light");
  light.className = `light ${data.verdict}`;
  light.textContent = String(data.verdict || "").toUpperCase();
  document.getElementById("summary").textContent =
    `${data.summary || ""} (${data.claim_count || 0} claims)`;
  const issues = document.getElementById("issues");
  issues.innerHTML = "";
  const list = data.problematic_claims || [];
  if (!list.length) {
    issues.textContent = "No problematic claims flagged.";
    return;
  }
  for (const c of list) {
    const div = document.createElement("div");
    div.className = `claim ${c.status}`;
    div.innerHTML = `<strong>${LABELS[c.status] || c.status}</strong><div>${escapeHtml(c.text)}</div><div>${escapeHtml(c.note)}</div>`;
    issues.appendChild(div);
  }
}

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

document.getElementById("download").addEventListener("click", () => {
  if (!last?.report_markdown) return;
  const blob = new Blob([last.report_markdown], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "truth-serum-report.md";
  a.click();
  URL.revokeObjectURL(url);
});
