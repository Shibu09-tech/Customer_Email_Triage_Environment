/* app.js — Customer Email Triage Dashboard */
'use strict';

const BASE = '';  // Same origin
const TASK_DESCRIPTIONS = {
  'priority-triage': '🟢 Easy: Classify email priority only (urgent/high/medium/low/spam). Score = 1.0 exact, 0.5 adjacent.',
  'full-routing':    '🟡 Medium: Classify priority AND route to the right department. Score = 0.5×priority + 0.5×category.',
  'full-pipeline':   '🔴 Hard: Priority + routing + draft a professional reply. Score = 0.3×priority + 0.3×category + 0.4×reply quality.',
};

let lastResponse = null;
let currentHistory = [];

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Nav tabs
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
    });
  });

  // JSON sub-tabs
  document.querySelectorAll('.json-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.json-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.json-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(`panel-${tab.dataset.panel}`).classList.add('active');
    });
  });

  // Task description
  const taskSelect = document.getElementById('taskSelect');
  taskSelect.addEventListener('change', updateTaskDescription);
  updateTaskDescription();

  // Buttons
  document.getElementById('btnReset').addEventListener('click', doReset);
  document.getElementById('btnStep').addEventListener('click', doStep);
  document.getElementById('btnState').addEventListener('click', doState);
  document.getElementById('btnCopyJson').addEventListener('click', copyJsonResponse);
});

function updateTaskDescription() {
  const task = document.getElementById('taskSelect').value;
  document.getElementById('taskDescription').textContent = TASK_DESCRIPTIONS[task] || '';
}

// ── API Calls ─────────────────────────────────────────────────────────────────

async function doReset() {
  const task = document.getElementById('taskSelect').value;
  setStatus('Resetting episode…', '');
  currentHistory = [];
  try {
    const res = await fetch(`${BASE}/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task }),
    });
    const data = await res.json();
    lastResponse = data;
    renderJsonRaw(data);
    renderObservation(data.observation);
    updateStats(data.observation, { done: false, reward: 0 });
    document.getElementById('btnStep').disabled = false;
    setStatus(`✓ Episode started — ${data.total_emails} emails to triage`, 'ok');
    setRewardDisplay('—', 'false');
    renderBreakdown(null);
  } catch (e) {
    setStatus(`✗ Reset failed: ${e.message}`, 'err');
  }
}

async function doStep() {
  const priority = document.getElementById('prioritySelect').value;
  const category = document.getElementById('categorySelect').value;
  const reply_draft = document.getElementById('replyDraft').value;
  const action = { priority, category, reply_draft };

  setStatus('Taking step…', '');
  try {
    const res = await fetch(`${BASE}/step`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(action),
    });
    const data = await res.json();
    lastResponse = data;
    renderJsonRaw(data);
    setRewardDisplay(data.reward.toFixed(2), data.done.toString());
    renderBreakdown(data.reward_breakdown);

    if (data.observation) {
      renderObservation(data.observation);
      updateStats(data.observation, data);
      setStatus(`✓ Step complete. Reward: ${data.reward.toFixed(4)}`, 'ok');
    } else if (data.done) {
      showEpisodeDone(data);
    }

    // Add to history
    if (data.info && data.info.email_id) {
      currentHistory.unshift({
        step: data.info.grader_scores ? Object.keys(currentHistory).length + 1 : '?',
        emailId: data.info.email_id,
        action,
        scores: data.info.grader_scores,
        reward: data.reward,
        done: data.done,
        truth: data.info.ground_truth,
      });
      renderHistory();
    }

    if (data.done) {
      document.getElementById('btnStep').disabled = true;
      document.getElementById('statDone').innerHTML = '<span class="badge badge-done">Done</span>';
    }
  } catch (e) {
    setStatus(`✗ Step failed: ${e.message}`, 'err');
  }
}

async function doState() {
  setStatus('Fetching state…', '');
  try {
    const res = await fetch(`${BASE}/state`);
    const data = await res.json();
    lastResponse = data;
    renderJsonRaw(data);
    setStatus('✓ State retrieved', 'ok');
  } catch (e) {
    setStatus(`✗ State fetch failed: ${e.message}`, 'err');
  }
}

// ── Rendering ─────────────────────────────────────────────────────────────────

function renderObservation(obs) {
  if (!obs) return;
  document.getElementById('emailPlaceholder').classList.add('hidden');
  const content = document.getElementById('emailContent');
  content.classList.remove('hidden');

  document.getElementById('emailSender').textContent = obs.sender;
  document.getElementById('emailThread').textContent = `${obs.thread_length} email(s)`;
  document.getElementById('emailSubject').textContent = obs.subject;
  document.getElementById('emailBody').textContent = obs.body;
  document.getElementById('emailMeta').textContent =
    `#${obs.email_id} · Step ${obs.step_number} · ${obs.emails_remaining} remaining`;

  const tierEl = document.getElementById('emailTier');
  tierEl.textContent = obs.sender_tier;
  tierEl.className = `field-value tier-badge tier-${obs.sender_tier}`;
}

function updateStats(obs, stepResult) {
  if (!obs) return;
  document.getElementById('statStep').textContent = obs.step_number ?? '—';
  document.getElementById('statLeft').textContent = obs.emails_remaining ?? '—';
  document.getElementById('statReward').textContent = obs.episode_reward_so_far?.toFixed(4) ?? '—';
  if (!stepResult.done) {
    document.getElementById('statDone').innerHTML = '<span class="badge badge-running">Running</span>';
  }
}

function setRewardDisplay(reward, done) {
  const rv = document.getElementById('rewardValue');
  if (rv) {
    rv.textContent = reward;
    rv.classList.add('reward-pulse');
    setTimeout(() => rv.classList.remove('reward-pulse'), 2000);
  }
  const dv = document.getElementById('doneValue');
  if (dv) dv.textContent = done;

  const topRv = document.getElementById('topRewardValue');
  if (topRv) {
    topRv.textContent = reward;
    if (reward !== '—') {
      topRv.style.color = 'var(--reward-color)';
    } else {
      topRv.style.color = 'var(--text-primary)';
    }
  }
  
  const topDv = document.getElementById('topDoneValue');
  if (topDv) {
    topDv.textContent = done;
    if (done === 'true') {
      topDv.style.color = 'var(--accent-red)';
    } else if (done === 'false') {
      topDv.style.color = 'var(--text-primary)';
    } else {
      topDv.style.color = 'var(--text-primary)';
    }
  }
}

function setStatus(msg, cls) {
  const el = document.getElementById('statusMsg');
  el.textContent = msg;
  el.className = `status-msg ${cls === 'ok' ? 'status-ok' : cls === 'err' ? 'status-err' : ''}`;
}

function renderJsonRaw(data) {
  document.getElementById('jsonRaw').textContent = JSON.stringify(data, null, 2);
}

function renderBreakdown(bd) {
  const el = document.getElementById('breakdownContent');
  if (!bd) {
    el.innerHTML = '<p class="muted">Take a step to see the reward breakdown.</p>';
    return;
  }
  el.innerHTML = `
    <div class="breakdown-grid">
      <div class="bd-item">
        <div class="bd-label">Priority</div>
        <div class="bd-value ${bd.priority_score > 0 ? 'bd-positive' : 'bd-negative'}">${bd.priority_score?.toFixed(2) ?? '—'}</div>
      </div>
      <div class="bd-item">
        <div class="bd-label">Category</div>
        <div class="bd-value ${bd.category_score > 0 ? 'bd-positive' : 'bd-negative'}">${bd.category_score?.toFixed(2) ?? '—'}</div>
      </div>
      <div class="bd-item">
        <div class="bd-label">Reply</div>
        <div class="bd-value ${bd.reply_score > 0 ? 'bd-positive' : 'bd-negative'}">${bd.reply_score?.toFixed(2) ?? '—'}</div>
      </div>
      <div class="bd-item">
        <div class="bd-label">Step Total</div>
        <div class="bd-value bd-neutral">${bd.total?.toFixed(4) ?? '—'}</div>
      </div>
    </div>
    <p style="margin-top:10px;font-size:0.75rem;color:var(--text-muted)">Step penalty: ${bd.step_penalty} (efficiency deduction)</p>
  `;
}

function renderHistory() {
  const el = document.getElementById('historyContent');
  if (currentHistory.length === 0) {
    el.innerHTML = '<p class="muted">Episode history will appear here.</p>';
    return;
  }
  el.innerHTML = currentHistory.map((h, i) => {
    const pCorrect = h.scores && h.truth && h.action.priority === h.truth.priority;
    const cCorrect = h.scores && h.truth && h.action.category === h.truth.category;
    return `
      <div class="history-item">
        <div class="history-step">Email ${h.emailId}</div>
        <div class="history-row">
          <span class="history-tag tag-priority">${h.action.priority}</span>
          <span class="history-tag tag-category">${h.action.category}</span>
          ${h.truth ? `<span class="history-tag ${pCorrect ? 'tag-correct' : 'tag-wrong'}">Priority: ${pCorrect ? '✓' : '✗ ' + h.truth.priority}</span>` : ''}
          ${h.truth ? `<span class="history-tag ${cCorrect ? 'tag-correct' : 'tag-wrong'}">Cat: ${cCorrect ? '✓' : '✗ ' + h.truth.category}</span>` : ''}
          <span class="history-tag tag-reward">+${h.reward.toFixed(4)}</span>
        </div>
      </div>
    `;
  }).join('');
}

function showEpisodeDone(data) {
  const summary = data.info?.episode_summary || {};
  setStatus(
    `🏁 Episode complete! Total reward: ${summary.total_reward ?? '?'} | Avg: ${summary.average_step_reward ?? '?'} | Success: ${summary.success ? '✅' : '❌'}`,
    'ok'
  );
  document.getElementById('emailPlaceholder').classList.remove('hidden');
  document.getElementById('emailContent').classList.add('hidden');
  document.getElementById('emailPlaceholder').innerHTML =
    `<div class="placeholder-icon">🏁</div>
     <p><strong>Episode Complete!</strong><br/>
     Total reward: <strong>${summary.total_reward ?? '?'}</strong><br/>
     Steps: ${summary.steps ?? '?'} | Avg: ${summary.average_step_reward ?? '?'}<br/>
     ${summary.success ? '✅ Success!' : '❌ Below threshold'}<br/><br/>
     Click <strong>Reset</strong> to start a new episode.</p>`;
}

function copyJsonResponse() {
  if (!lastResponse) return;
  navigator.clipboard.writeText(JSON.stringify(lastResponse, null, 2));
}

function copyCode(btn) {
  const code = btn.nextElementSibling.textContent;
  navigator.clipboard.writeText(code);
  btn.textContent = 'Copied!';
  setTimeout(() => btn.textContent = 'Copy', 1500);
}
