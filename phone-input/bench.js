(() => {
  const KEY = "pinkhouse.phone-input.v1";
  const COLOUR_KEY = "pinkhouse.phone-input.colour";
  const bench = document.getElementById("bench");
  const status = document.getElementById("status");
  const btnCopy = document.getElementById("btn-copy");
  const btnClear = document.getElementById("btn-clear");
  const btnColour = document.getElementById("btn-colour");

  if (!bench || !status || !btnCopy || !btnClear || !btnColour) return;

  let saveTimer = 0;
  let lastSaved = "";

  const stamp = () => {
    try {
      return new Intl.DateTimeFormat(undefined, {
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
      }).format(new Date());
    } catch {
      return new Date().toLocaleTimeString();
    }
  };

  const setStatus = (msg) => {
    status.textContent = msg;
  };

  const writeStore = (text) => {
    const payload = JSON.stringify({
      text,
      updatedAt: Date.now(),
    });
    localStorage.setItem(KEY, payload);
    lastSaved = text;
    setStatus(`Saved ${stamp()}. Still here if you leave.`);
  };

  const saveNow = () => {
    const text = bench.value;
    if (text === lastSaved) return;
    try {
      writeStore(text);
    } catch {
      setStatus("Could not save on this phone. Copy the words now.");
    }
  };

  const scheduleSave = () => {
    window.clearTimeout(saveTimer);
    saveTimer = window.setTimeout(saveNow, 180);
  };

  const load = () => {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) {
        setStatus("Ready. Words stay on this phone.");
        return;
      }
      const data = JSON.parse(raw);
      if (typeof data?.text === "string") {
        bench.value = data.text;
        lastSaved = data.text;
        setStatus(
          data.text
            ? `Restored. Last save was kept on this phone.`
            : "Ready. Words stay on this phone."
        );
      }
    } catch {
      setStatus("Ready. Could not read an old save.");
    }
  };

  const setColour = (on) => {
    document.body.classList.toggle("is-colour", on);
    btnColour.setAttribute("aria-pressed", on ? "true" : "false");
    try {
      localStorage.setItem(COLOUR_KEY, on ? "1" : "0");
    } catch {
      /* ignore */
    }
  };

  try {
    setColour(localStorage.getItem(COLOUR_KEY) === "1");
  } catch {
    setColour(false);
  }

  load();

  bench.addEventListener("input", scheduleSave);
  bench.addEventListener("change", saveNow);
  window.addEventListener("pagehide", saveNow);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") saveNow();
  });

  btnCopy.addEventListener("click", async () => {
    saveNow();
    const text = bench.value;
    if (!text) {
      setStatus("Nothing to copy yet.");
      return;
    }
    try {
      await navigator.clipboard.writeText(text);
      setStatus(`Copied ${stamp()}.`);
    } catch {
      bench.focus();
      bench.select();
      setStatus("Select and copy manually.");
    }
  });

  btnClear.addEventListener("click", () => {
    if (!bench.value) {
      setStatus("Already empty.");
      return;
    }
    const ok = window.confirm("Clear the bench? This cannot be undone on this phone.");
    if (!ok) return;
    bench.value = "";
    saveNow();
    setStatus("Cleared.");
    bench.focus();
  });

  btnColour.addEventListener("click", () => {
    setColour(!document.body.classList.contains("is-colour"));
  });

  // Keep the keyboard from covering the status after first focus on phones.
  bench.addEventListener("focus", () => {
    window.setTimeout(() => {
      bench.scrollIntoView({ block: "center", behavior: "smooth" });
    }, 300);
  });
})();
