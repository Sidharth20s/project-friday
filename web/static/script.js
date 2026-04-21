/**
 * FRIDAY AI Assistant — Frontend JavaScript
 * Handles WebSocket events, UI state, chat feed, and system stats.
 */

// ── SocketIO Connection ────────────────────────────────────
const socket = io();

// ── DOM References ────────────────────────────────────────
const bootScreen   = document.getElementById("bootScreen");
const bootLog      = document.getElementById("bootLog");
const statusDot    = document.getElementById("statusDot");
const statusText   = document.getElementById("statusText");
const connBadge    = document.getElementById("connBadge");
const chatFeed     = document.getElementById("chatFeed");
const textInput    = document.getElementById("textInput");
const waveform     = document.getElementById("waveform");
const waveformHint = document.getElementById("waveformHint");
const micBtn       = document.getElementById("micBtn");
const clockTime    = document.getElementById("clockTime");
const clockDate    = document.getElementById("clockDate");

// ── State ─────────────────────────────────────────────────
let currentState = "idle";
let typingBubble = null;
let statsInterval = null;

// ═══════════════════════════════════════════════════════════
// SOCKET EVENTS
// ═══════════════════════════════════════════════════════════

socket.on("connect", () => {
  setConnectionState(true);
  setStatus("idle", "FRIDAY Online — Ready");
  runBootSequence();
});

socket.on("disconnect", () => {
  setConnectionState(false);
  setStatus("error", "Connection lost — Reconnecting...");
});

socket.on("status_update", (data) => {
  setStatus(data.state, data.message);
});

socket.on("user_message_echo", (data) => {
  removeTypingIndicator();
  appendBubble("user", data.message);
});

socket.on("friday_reply", (data) => {
  removeTypingIndicator();
  appendBubble("friday", data.message);
  if (data.source === "voice") {
    setStatus("speaking", "Speaking...");
  }
});


// ═══════════════════════════════════════════════════════════
// UI STATE MANAGEMENT
// ═══════════════════════════════════════════════════════════

function setConnectionState(online) {
  if (online) {
    connBadge.textContent = "● ONLINE";
    connBadge.className = "connection-badge online";
  } else {
    connBadge.textContent = "● OFFLINE";
    connBadge.className = "connection-badge offline";
  }
}

function setStatus(state, message) {
  currentState = state;

  // Update dot
  statusDot.className = `status-indicator ${state}`;
  statusText.textContent = message;

  // Update waveform
  waveform.className = "waveform";
  if (state === "listening") {
    waveform.classList.add("listening");
    waveformHint.textContent = "🎤 Listening...";
    micBtn.classList.add("active");
  } else if (state === "speaking") {
    waveform.classList.add("speaking");
    waveformHint.innerHTML = '🔊 FRIDAY is speaking...';
    micBtn.classList.remove("active");
  } else if (state === "processing") {
    waveformHint.textContent = "⚙️ Processing...";
    micBtn.classList.remove("active");
    showTypingIndicator();
  } else if (state === "muted") {
    waveform.classList.add("muted");
    waveformHint.innerHTML = '<span style="color:var(--danger)">🔴 MICROPHONE MUTED</span>';
    micBtn.classList.add("muted");
  } else {
    waveformHint.innerHTML = 'Say <strong>"Hey Friday"</strong> or click the mic';
    micBtn.classList.remove("active");
    micBtn.classList.remove("muted");
  }
}


// ═══════════════════════════════════════════════════════════
// CHAT BUBBLES
// ═══════════════════════════════════════════════════════════

function appendBubble(role, text) {
  // Remove welcome message on first chat
  const welcome = chatFeed.querySelector(".chat-welcome");
  if (welcome) welcome.remove();

  const now = new Date().toLocaleTimeString("en-IN", {
    hour: "2-digit", minute: "2-digit"
  });

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${role}`;

  const avatar   = document.createElement("div");
  avatar.className = "bubble-avatar";
  avatar.textContent = role === "user" ? "👤" : "🤖";

  const content  = document.createElement("div");
  content.className = "bubble-content";

  const timeSpan = document.createElement("span");
  timeSpan.className = "bubble-time";
  timeSpan.textContent = now;

  // Render text with line breaks
  content.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");
  content.appendChild(timeSpan);

  bubble.appendChild(avatar);
  bubble.appendChild(content);

  chatFeed.appendChild(bubble);
  chatFeed.scrollTop = chatFeed.scrollHeight;
}

function showTypingIndicator() {
  if (typingBubble) return;

  typingBubble = document.createElement("div");
  typingBubble.className = "chat-bubble friday typing-indicator";
  typingBubble.id = "typingBubble";
  typingBubble.innerHTML = `
    <div class="bubble-avatar">🤖</div>
    <div class="bubble-content">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `;
  chatFeed.appendChild(typingBubble);
  chatFeed.scrollTop = chatFeed.scrollHeight;
}

function removeTypingIndicator() {
  if (typingBubble) {
    typingBubble.remove();
    typingBubble = null;
  }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}


// ═══════════════════════════════════════════════════════════
// USER INPUT
// ═══════════════════════════════════════════════════════════

function sendTextInput() {
  const msg = textInput.value.trim();
  if (!msg) return;

  appendBubble("user", msg);
  textInput.value = "";
  setStatus("processing", "Processing...");

  socket.emit("user_message", { message: msg });
}

function triggerVoice() {
  setStatus("listening", "Listening...");
  socket.emit("voice_trigger");
}

function sendQuick(command) {
  textInput.value = command;
  sendTextInput();
}

function clearMemory() {
  if (confirm("Clear FRIDAY's conversation memory?")) {
    socket.emit("clear_memory");
    chatFeed.innerHTML = `
      <div class="chat-welcome">
        <p>Memory cleared. Starting fresh.</p>
        <p>Type below or say <em>"Hey Friday"</em> to begin.</p>
      </div>
    `;
  }
}

function toggleMuteVisual() {
  if (currentState === "muted") {
    setStatus("idle", "Microphone Active");
  } else {
    setStatus("muted", "Microphone Muted");
  }
}

function updateVisionFeed(type, imageUrl) {
  const feed = document.getElementById(`${type}Feed`);
  if (!feed) return;
  feed.innerHTML = `<img src="${imageUrl}" style="width:100%; height:100%; object-fit:cover;">`;
}

// Enter key to send
textInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendTextInput();
  }
});

// Mic button → voice trigger
waveform.addEventListener("click", triggerVoice);


// ═══════════════════════════════════════════════════════════
// SYSTEM STATS
// ═══════════════════════════════════════════════════════════

async function fetchStats() {
  try {
    const res  = await fetch("/api/status");
    const data = await res.json();

    updateBar("cpuBar",  "cpuVal",  data.cpu,  "%");
    updateBar("ramBar",  "ramVal",  data.ram,  "%");
    updateBar("diskBar", "diskVal", data.disk, "%");

    if (data.battery) {
      const plugged = data.battery.plugged ? "⚡" : "🔋";
      updateBar("batBar", "batVal", data.battery.percent, `% ${plugged}`);
    } else {
      document.getElementById("batVal").textContent = "N/A";
    }

    // Clock from server time
    clockTime.textContent = data.time;
    clockDate.textContent = data.date;

  } catch (e) {
    // Keep showing last values
  }
}

function updateBar(barId, valId, value, suffix) {
  const bar = document.getElementById(barId);
  const val = document.getElementById(valId);
  if (bar) bar.style.width = `${Math.min(100, value)}%`;
  if (val) val.textContent = `${Math.round(value)}${suffix}`;

  // Color bar red if high
  if (barId !== "batBar" && value > 85) {
    bar.style.background = "linear-gradient(90deg, #cc0022, #ff3355)";
    bar.style.boxShadow  = "0 0 6px #ff3355";
  }
}

// Update every 3 seconds
fetchStats();
statsInterval = setInterval(fetchStats, 3000);


// ═══════════════════════════════════════════════════════════
// LOCAL CLOCK (smooth ticking between server syncs)
// ═══════════════════════════════════════════════════════════

function tickLocalClock() {
  const now  = new Date();
  const time = now.toLocaleTimeString("en-IN", {
    hour: "2-digit", minute: "2-digit", second: "2-digit"
  });
  clockTime.textContent = time;
}
setInterval(tickLocalClock, 1000);


// ═══════════════════════════════════════════════════════════
// BOOT SEQUENCE
// ═══════════════════════════════════════════════════════════

function runBootSequence() {
  if (sessionStorage.getItem("booted")) {
    bootScreen.classList.add("hidden");
    return;
  }

  const logs = [
    "LOADING NEURAL NETWORKS...",
    "ESTABLISHING SECURE CONNECTION...",
    "CALIBRATING VOICE SYNTHESIZER...",
    "INITIALIZING WINDOWS ACTION ENGINE...",
    "LOADING GEMINI AI CORE v1.5...",
    "SYNCING LOCAL MEMORY...",
    "ALL SYSTEMS NOMINAL."
  ];

  let i = 0;
  const interval = setInterval(() => {
    if (i < logs.length) {
      const line = document.createElement("div");
      line.textContent = `> ${logs[i]}`;
      bootLog.appendChild(line);
      bootLog.scrollTop = bootLog.scrollHeight;
      i++;
    } else {
      clearInterval(interval);
      setTimeout(() => {
        bootScreen.classList.add("hidden");
        sessionStorage.setItem("booted", "true");
      }, 500);
    }
  }, 400);
}


// ═══════════════════════════════════════════════════════════
// PARTICLES
// ═══════════════════════════════════════════════════════════

function createParticles() {
  const container = document.getElementById("particles");
  for (let i = 0; i < 40; i++) {
    const p = document.createElement("div");
    p.className = "particle";
    const size = Math.random() * 4 + 1;
    p.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${Math.random() * 100}vw;
      animation-duration: ${Math.random() * 15 + 10}s;
      animation-delay: ${Math.random() * 15}s;
      opacity: ${Math.random() * 0.5 + 0.1};
      box-shadow: 0 0 ${size * 2}px var(--cyan);
    `;
    container.appendChild(p);
  }
}
createParticles();


// ═══════════════════════════════════════════════════════════
// HEX GRID GLOW EFFECT (mouse interaction)
// ═══════════════════════════════════════════════════════════

document.addEventListener("mousemove", (e) => {
  const x = (e.clientX / window.innerWidth  * 100).toFixed(1);
  const y = (e.clientY / window.innerHeight * 100).toFixed(1);
  document.body.style.setProperty("--mx", `${x}%`);
  document.body.style.setProperty("--my", `${y}%`);
});
