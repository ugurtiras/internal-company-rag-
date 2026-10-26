"use strict";

const state = { roles: [], defaultTopK: 5 };

function el(id) {
  return document.getElementById(id);
}

function chipsFor(labels, container) {
  container.replaceChildren(
    ...labels.map((label) => {
      const span = document.createElement("span");
      span.className = "chip";
      span.textContent = label;
      return span;
    })
  );
}

async function loadRoles() {
  const response = await fetch("/api/roles");
  const data = await response.json();
  state.roles = data.roles;
  state.defaultTopK = data.default_top_k;

  const select = el("role");
  for (const item of data.roles) {
    const option = document.createElement("option");
    option.value = item.role;
    option.textContent = item.role;
    select.appendChild(option);
  }
  select.addEventListener("change", updateRoleLabels);

  const kSelect = el("k");
  for (let k = 1; k <= 10; k += 1) {
    const option = document.createElement("option");
    option.value = String(k);
    option.textContent = k;
    kSelect.appendChild(option);
  }
  kSelect.value = String(Math.min(10, Math.max(1, state.defaultTopK)));

  updateRoleLabels();
}

function updateRoleLabels() {
  const role = el("role").value;
  const item = state.roles.find((entry) => entry.role === role);
  chipsFor(item ? item.labels : [], el("role-labels"));
}

async function ask() {
  const role = el("role").value;
  const question = el("question").value.trim();
  const k = Number(el("k").value);
  const button = el("ask");
  const error = el("error");
  error.hidden = true;
  if (!question) {
    error.textContent = "Lütfen bir soru yazın.";
    error.hidden = false;
    return;
  }
  button.disabled = true;
  el("status").textContent = "Aranıyor…";
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role, question, k }),
    });
    const data = await response.json();
    if (!response.ok) {
      showError(data.error || "İstek başarısız.");
      return;
    }
    renderResults(data);
  } catch (err) {
    showError("Sunucuya ulaşılamadı.");
  } finally {
    button.disabled = false;
  }
}

function showError(message) {
  const error = el("error");
  error.textContent = message;
  error.hidden = false;
  el("status").textContent = "";
  el("result-list").replaceChildren();
}

function renderResults(data) {
  const list = el("result-list");
  list.replaceChildren();
  chipsFor(data.allowed_labels, el("role-labels"));
  if (data.results.length === 0) {
    el("status").textContent = "Erişim izniniz olan bir kaynak bulunamadı.";
    return;
  }
  el("status").textContent = data.results.length + " sonuç (k=" + data.k + ")";
  for (const item of data.results) {
    const card = document.createElement("article");
    card.className = "result";

    const meta = document.createElement("div");
    meta.className = "meta";
    const rank = document.createElement("span");
    rank.className = "rank";
    rank.textContent = String(item.rank);
    const doc = document.createElement("span");
    doc.className = "doc";
    doc.textContent = "[" + item.doc_id + "]";
    const section = document.createElement("span");
    section.textContent = item.section || "—";
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = item.access_label;
    const score = document.createElement("span");
    score.textContent = "skor " + item.score.toFixed(4);
    meta.append(rank, doc, section, chip, score);

    const snippet = document.createElement("p");
    snippet.className = "snippet";
    snippet.textContent = item.snippet;

    card.append(meta, snippet);
    list.appendChild(card);
  }
}

el("ask").addEventListener("click", ask);
el("question").addEventListener("keydown", (event) => {
  if (event.key === "Enter") ask();
});

loadRoles().catch(() => showError("Rol listesi alınamadı — sunucunun çalıştığından emin olun."));
