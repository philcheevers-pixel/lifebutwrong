(() => {
  const textEl = document.getElementById("text");
  const fileEl = document.getElementById("file");
  const runBtn = document.getElementById("run");
  const errorEl = document.getElementById("error");
  const wordCount = document.getElementById("word-count");
  const loading = document.getElementById("loading");
  const results = document.getElementById("results");
  const inputPanel = document.getElementById("input-panel");
  let lastResult = null;
  let lastText = "";

  const STATUS_LABEL = {
    supported: "Supported",
    unsupported: "Unsupported / weakly supported",
    unclear: "Unclear / needs more context",
    conflation: "Possible conflation or leap",
  };

  const KOFI = (window.TRUTHSERUM_KOFI_URL || "https://ko-fi.com/").trim();
  document.getElementById("kofi").href = KOFI;

  function words(text) {
    const t = text.trim();
    return t ? t.split(/\s+/).length : 0;
  }

  function updateCount() {
    wordCount.textContent = `${words(textEl.value).toLocaleString()} words`;
  }

  function showError(msg) {
    errorEl.hidden = !msg;
    errorEl.textContent = msg || "";
  }

  fileEl.addEventListener("change", async () => {
    const file = fileEl.files && fileEl.files[0];
    if (!file) return;
    // For txt/md preview in textarea; PDF/DOCX go straight via FormData on submit.
    if (/\.(txt|md|markdown)$/i.test(file.name)) {
      textEl.value = await file.text();
      updateCount();
    }
  });

  textEl.addEventListener("input", updateCount);
  updateCount();

  function downloadBlob(filename, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  function render(result) {
    lastResult = result;
    const light = document.getElementById("light");
    light.className = `light ${result.verdict}`;
    light.textContent = result.verdict.toUpperCase();
    document.getElementById("summary").textContent = result.summary;
    document.getElementById("meta").textContent =
      `${result.claim_count} claims · mode: ${result.mode}` +
      (result.rate_limit_remaining != null ? ` · runs left today: ${result.rate_limit_remaining}` : "");

    const bd = document.getElementById("breakdown");
    bd.innerHTML = "";
    for (const [key, label] of Object.entries(STATUS_LABEL)) {
      const n = (result.breakdown && result.breakdown[key]) || 0;
      const div = document.createElement("div");
      div.innerHTML = `<strong>${n}</strong><span>${label}</span>`;
      bd.appendChild(div);
    }

    const issues = document.getElementById("issues");
    issues.innerHTML = "";
    const list = result.problematic_claims || [];
    if (!list.length) {
      issues.innerHTML = "<p>No problematic claims flagged.</p>";
    } else {
      for (const c of list) {
        const art = document.createElement("article");
        art.className = `claim ${c.status}`;
        art.innerHTML = `
          <div class="status">${STATUS_LABEL[c.status] || c.status}</div>
          <p><strong>Claim:</strong> ${escapeHtml(c.text)}</p>
          <p><strong>Note:</strong> ${escapeHtml(c.note)}</p>
        `;
        issues.appendChild(art);
      }
    }

    inputPanel.hidden = true;
    loading.hidden = true;
    results.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  runBtn.addEventListener("click", async () => {
    showError("");
    runBtn.disabled = true;
    loading.hidden = false;
    results.hidden = true;
    try {
      const fd = new FormData();
      const file = fileEl.files && fileEl.files[0];
      if (file && !/\.(txt|md|markdown)$/i.test(file.name)) {
        fd.append("file", file, file.name);
        lastText = "";
      } else {
        const text = textEl.value.trim();
        if (!text) throw new Error("Paste some text or choose a file.");
        fd.append("text", text);
        lastText = text;
      }
      const res = await fetch("/analyze", { method: "POST", body: fd });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || data.error || `Request failed (${res.status})`);
      if (!lastText && data.claims) {
        // keep markdown download working from embedded report
        lastText = textEl.value.trim();
      }
      render(data);
    } catch (err) {
      loading.hidden = false;
      loading.hidden = true;
      inputPanel.hidden = false;
      showError(err.message || String(err));
    } finally {
      runBtn.disabled = false;
    }
  });

  document.getElementById("download-md").addEventListener("click", () => {
    if (!lastResult) return;
    downloadBlob("truth-serum-report.md", lastResult.report_markdown || "", "text/markdown");
  });
  document.getElementById("download-html").addEventListener("click", () => {
    if (!lastResult) return;
    downloadBlob("truth-serum-report.html", lastResult.report_html || "", "text/html");
  });
  document.getElementById("again").addEventListener("click", () => {
    results.hidden = true;
    inputPanel.hidden = false;
    showError("");
  });
})();
