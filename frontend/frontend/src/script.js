
/* CareerMatch AI - connected to the FastAPI backend */

const CONFIG = {
  BASE_URL: (
    window.CAREERMATCH_API_URL || "http://127.0.0.1:8000"
  ).replace(/\/+$/, ""),
  HEALTH: "/api/health",
  RESUME_UPLOAD: "/api/resume/upload",
  MATCHING: "/api/matching/run",
  JOBS: "/api/jobs",
  RECRUITER: "/api/recruiter/rank-candidates",
};

const $ = (id) => document.getElementById(id);

let mode = "student";

const SAMPLES = {
  student:
    "Computer science student skilled in Python, SQL, machine learning, pandas and scikit-learn. Built a movie recommender and a sales dashboard.",
  recruiter:
    "Recruiter mode requires an existing job ID.",
};

const LABELS = {
  student: "Resume text (upload a file below to run matching)",
  recruiter: "Job description (requires an existing job ID)",
};

const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[c]);

const pct = (v) => {
  const n = Number(v) || 0;
  return Math.max(0, Math.min(100, Math.round(n <= 1 ? n * 100 : n)));
};

const color = (p) =>
  p >= 70 ? "var(--good)" : p >= 45 ? "var(--warn)" : "var(--bad)";

function normalize(r) {
  return {
    title:
      r.title ||
      r.job_title ||
      r.name ||
      r.candidate_name ||
      r.filename ||
      "Untitled",
    company: r.company || r.organization || "",
    location: r.location || "",
    score: pct(r.final_score ?? r.score ?? r.match_score),
    semantic: pct(r.semantic_score ?? r.semantic),
    skills: pct(r.skill_score ?? r.skills_score),
    evidence: pct(r.evidence_score ?? r.evidence),
    have: Array.isArray(r.matched_skills)
      ? r.matched_skills
      : Array.isArray(r.have_skills)
        ? r.have_skills
        : [],
    missing: Array.isArray(r.missing_skills)
      ? r.missing_skills
      : Array.isArray(r.skills_to_learn)
        ? r.skills_to_learn
        : [],
    rec: r.recommendation || r.explanation || "",
    url: r.url || r.link || r.apply_url || r.source_url || "",
  };
}

async function readResponse(res) {
  const raw = await res.text();
  let data;

  try {
    data = raw ? JSON.parse(raw) : {};
  } catch {
    data = { detail: raw };
  }

  if (!res.ok) {
    const detail =
      data?.detail || data?.message || raw || "Unknown server error";
    throw new Error(`HTTP ${res.status}: ${detail}`);
  }

  return data;
}

async function checkApi() {
  const el = $("status");
  if (!el) return;

  try {
    const res = await fetch(CONFIG.BASE_URL + CONFIG.HEALTH);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    el.textContent = "● API online";
    el.className = "badge ok";
  } catch {
    el.textContent = "● API offline";
    el.className = "badge off";
  }
}

/* Tabs */
document.querySelectorAll(".tab").forEach((btn) => {
  btn.onclick = () => {
    document.querySelectorAll(".tab").forEach((b) =>
      b.classList.remove("active")
    );

    btn.classList.add("active");
    mode = btn.dataset.mode;

    if ($("inputLabel")) {
      $("inputLabel").textContent = LABELS[mode];
    }

    $("results").innerHTML = "";
    $("error").classList.add("hidden");

    $("sample").textContent =
      mode === "student" ? "Use sample" : "Show recruiter instructions";

    $("run").textContent =
      mode === "student" ? "Find matches" : "Rank candidates";
  };
});

$("sample").onclick = () => {
  $("text").value = SAMPLES[mode];

  if (mode === "recruiter") {
    showError(
      "Recruiter ranking requires an existing numeric job_id. " +
      "Use GET /api/jobs to find job IDs."
    );
  }
};

$("file").onchange = (e) => {
  $("fileName").textContent = e.target.files[0]
    ? "📎 " + e.target.files[0].name
    : "📄 Or drop / choose a PDF, DOCX or TXT file";
};

$("run").onclick = run;

/* Main action */
async function run() {
  $("error").classList.add("hidden");

  if (mode === "recruiter") {
    showError(
      "Recruiter ranking requires a saved job_id. " +
      "The current page does not have a job ID selector. " +
      "Create or select a job using POST/GET /api/jobs first."
    );
    return;
  }

  const file = $("file").files[0];

  if (!file) {
    showError(
      "Please choose a PDF, DOCX, or TXT resume file. " +
      "The current backend upload endpoint requires a file."
    );
    return;
  }

  const topK = Math.max(
    1,
    Math.min(100, Number($("topk").value) || 10)
  );

  $("run").disabled = true;
  $("run").textContent = "Uploading resume…";
  $("results").innerHTML =
    '<div class="skeleton"></div>'.repeat(3);

  try {
    // Step 1: Upload the resume.
    const form = new FormData();
    form.append("file", file);

    const uploadRes = await fetch(
      CONFIG.BASE_URL + CONFIG.RESUME_UPLOAD,
      {
        method: "POST",
        body: form,
      }
    );

    const uploadData = await readResponse(uploadRes);

    const resumeId = uploadData.resume_id ?? uploadData.id;

    if (resumeId == null) {
      throw new Error(
        "Resume upload succeeded, but the response did not contain resume_id. " +
        "Check the response from POST /api/resume/upload."
      );
    }

    // Step 2: Run matching using the saved resume ID.
    $("run").textContent = "Finding matches…";

    const params = new URLSearchParams({
      resume_id: String(resumeId),
      top_k: String(topK),
    });

    const matchRes = await fetch(
      `${CONFIG.BASE_URL}${CONFIG.MATCHING}?${params.toString()}`,
      {
        method: "POST",
      }
    );

    const matchData = await readResponse(matchRes);

    const rawList = Array.isArray(matchData)
      ? matchData
      : matchData.matches || matchData.results || [];

    render(rawList.map(normalize));
  } catch (e) {
    $("results").innerHTML = "";

    showError(
      e.message.includes("Failed to fetch")
        ? "Cannot reach the backend. Ensure Uvicorn is running at " +
          "http://127.0.0.1:8000 and CORS allows this frontend."
        : e.message
    );
  } finally {
    $("run").disabled = false;
    $("run").textContent =
      mode === "student" ? "Find matches" : "Rank candidates";
  }
}

function showError(msg) {
  const el = $("error");
  el.textContent = "⚠️ " + msg;
  el.classList.remove("hidden");
}

/* Display matching results */
function render(list) {
  if (!list.length) {
    $("results").innerHTML =
      "<h2>No matches found</h2>" +
      "<p>Check whether the application database contains jobs " +
      "synchronized with the FAISS index.</p>";
    return;
  }

  const chart = list
    .map(
      (m) => `
        <div class="crow">
          <span class="t">${esc(m.title)}</span>
          <div class="track">
            <div class="fill" style="width:${m.score}%;background:${color(m.score)}"></div>
          </div>
          <b>${m.score}%</b>
        </div>
      `
    )
    .join("");

  const cards = list
    .map(
      (m) => `
        <article class="card match">
          <div class="ring" style="--p:${m.score};--c:${color(m.score)}">
            <b>${m.score}%</b>
          </div>
          <div>
            <h3>${esc(m.title)}</h3>
            <div class="sub">
              ${esc(m.company)}
              ${m.location ? ` · ${esc(m.location)}` : ""}
            </div>
            <div class="bars">
              ${bar("Semantic", m.semantic)}
              ${bar("Skills", m.skills)}
              ${bar("Evidence", m.evidence)}
            </div>
            ${
              m.have.length
                ? `<div class="chips">${m.have
                    .map(
                      (s) =>
                        `<span class="chip have">✓ ${esc(s)}</span>`
                    )
                    .join("")}</div>`
                : ""
            }
            ${
              m.missing.length
                ? `<div class="chips">${m.missing
                    .map(
                      (s) =>
                        `<span class="chip miss">+ ${esc(s)}</span>`
                    )
                    .join("")}</div>`
                : ""
            }
            ${m.rec ? `<p class="rec">${esc(m.rec)}</p>` : ""}
            ${
              m.url
                ? `<a class="link" href="${esc(m.url)}" target="_blank" rel="noopener noreferrer">View posting →</a>`
                : ""
            }
          </div>
        </article>
      `
    )
    .join("");

  $("results").innerHTML =
    `<h2>Ranking</h2>` +
    `<div class="card chart">${chart}</div>` +
    `<h2>Detailed matches</h2>${cards}`;
}

function bar(label, p) {
  return `
    <div>
      <small>${label} · ${p}%</small>
      <div class="track">
        <div class="fill" style="width:${p}%;background:${color(p)}"></div>
      </div>
    </div>
  `;
}

checkApi();
