const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:8000' : '';

// Global State
let currentTheme = localStorage.getItem('theme') || 'dark';
let bookmarks = JSON.parse(localStorage.getItem('bookmarks')) || [];
let glossaryData = [];
let quizData = [];
let userAnswers = {};
let flashcardState = {
    active: false,
    terms: [],
    currentIndex: 0,
    flipped: false
};

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    renderBookmarks();

    // Initial Load based on active tab
    // Default is overview, no specific load needed

    // Event Listeners for global UI
    document.getElementById('glossary-search').addEventListener('input', (e) => filterGlossary(e.target.value));
    document.getElementById('glossary-filter').addEventListener('change', (e) => filterGlossary(document.getElementById('glossary-search').value));

    // Initialize News Feed
    loadNews();
});

// --- Theme Logic ---
function loadTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');

    if (currentTheme === 'light') {
        html.classList.add('light-mode'); // We can add specific light mode utility class if needed, or just handle via CSS variables
        // For Tailwind dark mode, we usually toggle 'dark' class. 
        // But here the base is dark. Let's assume we might inverse colors or just keep it simple for now.
        // Given existing CSS is hardcoded colors, 'light mode' might require more CSS work.
        // Let's implement a "Reading Mode" which makes text higher contrast if not full light theme.
        // For now, let's toggle a simple class and user style.
        document.body.style.backgroundColor = '#f8fafc';
        document.body.style.color = '#0f172a';
        // We'd need to override a lot of "text-white" classes. 
        // Since we didn't do full CSS variable refactor, let's make this a "High Contrast" mode instead?
        // Or actually, let's just stick to the requested "Dark/Light" but acknowledge limitations.
        // Better: Let's swap the background and text colors dynamically for the main containers.
    } else {
        document.body.style.backgroundColor = '#0f172a';
        document.body.style.color = '#f8fafc';
    }
}

function toggleTheme() {
    currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', currentTheme);
    loadTheme();
    // Force reload to apply styles properly if we had a full CSS framework
    // For this simple version, we'll reload to ensure clean state or just run loadTheme
    location.reload();
}

// --- Navigation ---
function switchTab(tab) {
    // Hide all views
    document.querySelectorAll('[id^="view-"]').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active', 'bg-blue-600/20', 'text-blue-400'));

    // Show selected
    document.getElementById(`view-${tab}`).classList.remove('hidden');

    // Highlight nav
    const navBtn = document.getElementById(`nav-${tab}`);
    if (navBtn) navBtn.classList.add('active', 'bg-blue-600/20', 'text-blue-400');

    // Specific logic
    if (tab === 'student') {
        loadQuiz();
        loadCareer();
        showCheat('ports'); // Default cheat sheet
    }
}

// --- Core Scanners (File/URL) ---
function handleFileSelect(input) {
    const fileLabel = document.getElementById('file-label');
    if (input.files.length > 0) {
        fileLabel.textContent = input.files[0].name;
    }
}

async function scanFile() {
    const input = document.getElementById('file-input');
    if (!input.files[0]) return alert("Please select a file");

    toggleLoader(true);
    const formData = new FormData();
    formData.append('file', input.files[0]);

    try {
        const res = await fetch(`${API_BASE}/api/scan/file`, {
            method: 'POST', body: formData
        });
        const data = await res.json();
        renderReport('file', data);
    } catch (e) {
        alert("Scan failed: " + e.message);
    } finally {
        toggleLoader(false);
    }
}

async function scanUrl() {
    const url = document.getElementById('url-input').value;
    const consent = document.getElementById('consent-check').checked;

    if (!url) return alert("Enter a URL");
    if (!consent) return alert("You must verify authorization");

    toggleLoader(true);
    try {
        const res = await fetch(`${API_BASE}/api/scan/url`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await res.json();
        renderReport('url', data);
    } catch (e) {
        alert("Scan failed: " + e.message);
    } finally {
        toggleLoader(false);
    }
}

function toggleLoader(show) {
    const views = ['view-overview', 'view-dashboard', 'view-tools', 'view-phishing', 'view-student', 'view-education'];
    document.getElementById('loader').classList.toggle('hidden', !show);
    // Hide scan cards if loading
    document.querySelector('#view-dashboard > .grid').classList.toggle('hidden', show);
}

function renderReport(type, data) {
    switchTab('report');

    // Risk Badge
    const badge = document.getElementById('report-risk-badge');
    badge.textContent = data.risk_level || 'UNKNOWN';
    badge.className = `px-3 py-1 rounded-full text-xs font-bold ${getRiskColor(data.risk_level)}`;

    document.getElementById('report-target').textContent = normalizeTarget(data);
    document.getElementById('report-summary').textContent = generateSummary(type, data);

    // Details
    const detailsList = document.getElementById('report-details');
    detailsList.innerHTML = '';

    Object.entries(data).forEach(([key, val]) => {
        if (['risk_level', 'filename', 'url'].includes(key)) return;

        let content = val;
        if (typeof val === 'object') content = JSON.stringify(val, null, 2);
        if (Array.isArray(val)) content = val.join(', ');

        const li = document.createElement('li');
        li.className = "text-sm text-slate-300 border-b border-slate-700 pb-2";
        li.innerHTML = `<span class="font-bold text-blue-400 capitalize">${key.replace(/_/g, ' ')}:</span> <span class="font-mono text-xs">${content}</span>`;
        detailsList.appendChild(li);
    });

    // Remediation
    const remList = document.getElementById('report-remediation');
    remList.innerHTML = getRemediation(data).map(r =>
        `<li class="flex gap-2 text-sm text-slate-300"><span class="text-green-500">âœ”</span> ${r}</li>`
    ).join('');
}

function getRiskColor(level) {
    if (level === 'HIGH') return 'bg-red-500/20 text-red-400 border border-red-500/50';
    if (level === 'MEDIUM') return 'bg-orange-500/20 text-orange-400 border border-orange-500/50';
    return 'bg-green-500/20 text-green-400 border border-green-500/50';
}

function normalizeTarget(data) {
    return data.filename ? `File: ${data.filename}` : `URL: ${data.url}`;
}

function generateSummary(type, data) {
    if (type === 'file') {
        return `File analysis completed with ${data.risk_level} risk assessment. Entropy score indicates ${data.entropy > 7 ? 'possible encryption/packing' : 'standard data structure'}.`;
    }
    return `Passive scan of ${data.url} complete. Site ${data.https ? 'uses HTTPS' : 'lacks HTTPS encryption'}. Found ${data.missing_security_headers?.length || 0} missing security headers.`;
}

function getRemediation(data) {
    const steps = [];
    if (data.risk_level === 'HIGH') steps.push("Immediate investigation required.");
    if (data.missing_security_headers?.length) steps.push("Configure missing HTTP security headers (HSTS, CSP).");
    if (!data.https && data.url) steps.push("Enforce HTTPS with a valid SSL certificate.");
    if (data.entropy > 7) steps.push("File may be packed/obfuscated. Run in sandbox.");
    if (steps.length === 0) steps.push("No immediate actions required. Continue monitoring.");
    return steps;
}

// --- Tools Logic ---
async function checkPassword() {
    const pwd = document.getElementById('pass-input').value;
    const mode = document.getElementById('attack-mode').value;
    const hw = document.getElementById('attack-hardware').value;
    const hash = document.getElementById('attack-hash').value;

    if (!pwd) return;

    const res = await fetch(`${API_BASE}/api/tools/password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            password: pwd,
            attack_mode: mode,
            hardware: hw,
            hash_type: hash
        })
    });
    const data = await res.json();

    document.getElementById('pass-result').classList.remove('hidden');
    document.getElementById('pass-rating').textContent = `${data.score}/4`;
    document.getElementById('pass-entropy').textContent = `${data.entropy} bits`;
    document.getElementById('pass-time').textContent = data.crack_time_estimate;

    // Show guesses/sec context if available
    if (data.guesses_per_second) {
        const rate = data.guesses_per_second.toLocaleString();
        document.getElementById('pass-time').title = `Assumed Rate: ${rate} guesses/sec`;
    }
}

function toggleOfflineOpts() {
    const mode = document.getElementById('attack-mode').value;
    const opts = document.getElementById('offline-opts');
    if (mode === 'online') opts.classList.add('opacity-50', 'pointer-events-none');
    else opts.classList.remove('opacity-50', 'pointer-events-none');
}

async function calcHash() {
    const text = document.getElementById('hash-input').value;
    if (!text) return;

    const res = await fetch(`${API_BASE}/api/tools/hash`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    const data = await res.json();

    document.getElementById('hash-result').classList.remove('hidden');
    document.getElementById('hash-md5').textContent = data.md5;
    document.getElementById('hash-sha256').textContent = data.sha256;
}

// --- Phishing Logic ---
async function scanPhishUrl() {
    const url = document.getElementById('phish-url-input').value;
    if (!url) return;

    const res = await fetch(`${API_BASE}/api/tools/phishing/url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    });
    const data = await res.json();

    document.getElementById('phish-url-result').classList.remove('hidden');
    document.getElementById('phish-url-risk').textContent = data.prediction;
    document.getElementById('phish-url-conf').textContent = `${(data.confidence * 100).toFixed(1)}%`;
    document.getElementById('phish-url-reason').textContent = "Based on lexical features (length, special chars, domain age request).";
}

async function scanEmail() {
    const subject = document.getElementById('email-subject').value;
    const body = document.getElementById('email-body').value;

    const res = await fetch(`${API_BASE}/api/tools/phishing/email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject, body })
    });
    const data = await res.json();

    document.getElementById('email-result').classList.remove('hidden');
    const riskEl = document.getElementById('email-risk');
    riskEl.textContent = data.risk_level;
    riskEl.className = `font-bold ml-2 ${data.risk_level === 'HIGH' ? 'text-red-500' : 'text-green-500'}`;

    const list = document.getElementById('email-triggers');
    list.innerHTML = data.triggers.map(t => `<li>${t}</li>`).join('') || "<li>No specific triggers found.</li>";
}

// --- Student Zone Logic ---
async function loadQuiz() {
    const difficulty = document.getElementById('quiz-difficulty').value;
    // We fetch all then filter client side for now as API returns random set
    // A better API would allow filtering params. Let's filter on Client for now or just fetch random.
    const res = await fetch(`${API_BASE}/api/education/quiz`); // Random 5
    quizData = await res.json();

    if (difficulty !== 'All') {
        quizData = quizData.filter(q => q.difficulty === difficulty);
    }

    userAnswers = {};
    const container = document.getElementById('quiz-container');
    container.innerHTML = '';

    if (quizData.length === 0) {
        container.innerHTML = `<p class="text-slate-500">No questions found for ${difficulty} difficulty. Try another level.</p>`;
        return;
    }

    quizData.forEach((q, idx) => {
        const qDiv = document.createElement('div');
        qDiv.className = "p-4 bg-slate-800/50 rounded border border-slate-700";
        qDiv.innerHTML = `
            <div class="flex justify-between mb-2">
                <span class="text-xs font-bold px-2 py-0.5 rounded bg-slate-700 ${getDiffColor(q.difficulty)}">${q.difficulty || 'Medium'}</span>
                <span class="text-xs text-slate-500">Q${idx + 1}</span>
            </div>
            <p class="text-white font-medium mb-3">${q.question}</p>
            <div class="space-y-2">
                ${q.options.map((opt, oIdx) => `
                    <button onclick="selectAnswer(${idx}, ${oIdx}, this)" 
                        class="w-full text-left p-2 rounded bg-slate-700 hover:bg-slate-600 text-sm transition-colors"
                        id="q${idx}-opt${oIdx}">
                        ${opt}
                    </button>
                `).join('')}
            </div>
            <div id="q${idx}-exp" class="hidden mt-3 p-2 bg-slate-900/50 border-l-2 border-blue-500 text-xs text-slate-300">
                ${q.explanation || 'No explanation available.'}
            </div>
        `;
        container.appendChild(qDiv);
    });

    document.getElementById('quiz-score').classList.add('hidden');
}

function getDiffColor(diff) {
    if (diff === 'Easy') return 'text-green-400';
    if (diff === 'Hard') return 'text-red-400';
    return 'text-yellow-400';
}

function selectAnswer(qIdx, optIdx, btn) {
    if (userAnswers[qIdx] !== undefined) return; // Already answered

    userAnswers[qIdx] = optIdx;
    const q = quizData[qIdx];
    const isCorrect = optIdx === q.correct;

    // UI Feedback
    if (isCorrect) {
        btn.classList.add('bg-green-600', 'text-white', 'hover:bg-green-600');
    } else {
        btn.classList.add('bg-red-600', 'text-white', 'hover:bg-red-600');
        // Show correct
        document.getElementById(`q${qIdx}-opt${q.correct}`).classList.add('bg-green-600/50', 'text-white');
    }

    // Show Explanation
    document.getElementById(`q${qIdx}-exp`).classList.remove('hidden');

    // Check if all answered
    if (Object.keys(userAnswers).length === quizData.length) {
        showScore();
    }
}

function showScore() {
    let score = 0;
    quizData.forEach((q, i) => {
        if (userAnswers[i] === q.correct) score++;
    });

    document.getElementById('score-val').textContent = score;
    document.getElementById('quiz-score').classList.remove('hidden');
}

async function exportQuizPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(20);
    doc.text("Security Quiz Results", 105, 20, null, null, "center");

    doc.setFontSize(12);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 20, 30);

    let score = document.getElementById('score-val').textContent;
    doc.text(`Score: ${score}/${quizData.length}`, 20, 40);

    let y = 60;

    quizData.forEach((q, i) => {
        const userAnswer = userAnswers[i];
        const isCorrect = userAnswer === q.correct;
        const status = isCorrect ? "CORRECT" : "WRONG";

        doc.setFontSize(12);
        doc.setTextColor(isCorrect ? 0 : 200, isCorrect ? 150 : 0, 0);
        doc.text(`Q${i + 1}: ${status}`, 20, y);

        doc.setTextColor(0, 0, 0);
        doc.setFontSize(10);
        const splitQuestion = doc.splitTextToSize(q.question, 170);
        doc.text(splitQuestion, 20, y + 7);
        y += 10 + (splitQuestion.length * 5);

        doc.text(`Correct Check: ${q.options[q.correct]}`, 20, y);
        y += 15;

        if (y > 270) {
            doc.addPage();
            y = 20;
        }
    });

    doc.save("security_quiz_results.pdf");
}

async function loadCareer() {
    const res = await fetch(`${API_BASE}/api/education/career`);
    const data = await res.json();
    const container = document.getElementById('career-container');
    container.innerHTML = data.map(phase => `
        <div class="border-l-2 border-slate-700 pl-4 pb-4">
            <h4 class="text-white font-bold">${phase.title}</h4>
            <p class="text-sm text-slate-400 mt-1">${phase.content}</p>
        </div>
    `).join('');
}

async function showCheat(type) {
    const res = await fetch(`${API_BASE}/api/education/cheatsheets`);
    const data = await res.json();
    const sheet = data[type];
    const container = document.getElementById('cheat-content');

    if (!sheet) return;

    let html = '';
    if (type === 'ports') {
        html = `<table class="w-full text-left text-sm">
            <thead class="text-slate-500 border-b border-slate-700"><tr><th class="p-2">Port</th><th class="p-2">Service</th><th class="p-2">Desc</th></tr></thead>
            <tbody>${sheet.map(r => `<tr><td class="p-2 text-blue-400 font-mono">${r.port}</td><td class="p-2 text-white">${r.service}</td><td class="p-2 text-slate-400">${r.desc}</td></tr>`).join('')}</tbody>
        </table>`;
    } else if (type === 'linux') {
        html = `<table class="w-full text-left text-sm">
            <thead class="text-slate-500 border-b border-slate-700"><tr><th class="p-2">Command</th><th class="p-2">Desc</th></tr></thead>
            <tbody>${sheet.map(r => `<tr><td class="p-2 text-green-400 font-mono">${r.cmd}</td><td class="p-2 text-slate-400">${r.desc}</td></tr>`).join('')}</tbody>
        </table>`;
    } else if (type === 'owasp') {
        html = `<ul class="space-y-3">${sheet.map(r => `
            <li class="p-2 bg-slate-800/50 rounded">
                <span class="text-red-400 font-bold block text-xs">${r.vuln}</span>
                <span class="text-slate-300 text-sm">${r.desc}</span>
            </li>
         `).join('')}</ul>`;
    } else {
        html = `<ul class="space-y-3">${sheet.map(r => `
            <li class="p-2 bg-slate-800/50 rounded">
                <span class="text-purple-400 font-bold block text-xs">${r.name}</span>
                <span class="text-slate-300 text-sm">${r.desc}</span>
            </li>
         `).join('')}</ul>`;
    }
    container.innerHTML = html;
}

function runCipher(encode) {
    const type = document.getElementById('cipher-type').value;
    const input = document.getElementById('cipher-input').value.toUpperCase();
    const keyInput = document.getElementById('cipher-key').value;
    let output = '';

    if (type === 'caesar') {
        const shift = encode ? 3 : -3 + 26; // +26 ensures positive mod
        output = input.replace(/[A-Z]/g, c => String.fromCharCode(((c.charCodeAt(0) - 65 + shift) % 26) + 65));
    } else if (type === 'rot13') {
        output = input.replace(/[A-Z]/g, c => String.fromCharCode(((c.charCodeAt(0) - 65 + 13) % 26) + 65));
    } else if (type === 'base64') {
        try {
            output = encode ? btoa(input) : atob(input);
        } catch (e) { output = "Invalid Base64"; }
    } else if (type === 'vigenere') {
        // Simple Vigenere implementation
        if (!keyInput) { output = "Key required"; }
        else {
            const key = keyInput.toUpperCase().replace(/[^A-Z]/g, '');
            let keyIdx = 0;
            output = input.replace(/[A-Z]/g, c => {
                const k = key.charCodeAt(keyIdx++ % key.length) - 65;
                const shift = encode ? k : (26 - k);
                return String.fromCharCode(((c.charCodeAt(0) - 65 + shift) % 26) + 65);
            });
        }
    }

    document.getElementById('cipher-output').textContent = output;
}

// Toggle key input for Vigenere
document.getElementById('cipher-type').addEventListener('change', (e) => {
    document.getElementById('cipher-key').classList.toggle('hidden', e.target.value !== 'vigenere');
});


// --- CyberPedia / Glossary Logic ---
async function loadGlossary() {
    const res = await fetch(`${API_BASE}/api/education/glossary`);
    glossaryData = await res.json();
    renderGlossary(glossaryData);
    setDailyTerm(glossaryData);
}

function filterGlossary(query) {
    const cat = document.getElementById('glossary-filter').value;
    const search = query.toLowerCase();

    const filtered = glossaryData.filter(item => {
        const matchSearch = item.term.toLowerCase().includes(search) || item.definition.toLowerCase().includes(search);
        const matchCat = cat === 'all' || item.category === cat;
        return matchSearch && matchCat;
    });
    renderGlossary(filtered);
}

function renderGlossary(data) {
    const grid = document.getElementById('glossary-grid');
    grid.innerHTML = '';

    data.forEach(item => {
        // Check bookmark status
        const isBookmarked = bookmarks.includes(item.term);

        const card = document.createElement('div');
        card.className = "glass-panel p-6 rounded-xl border border-slate-700/50 hover:border-blue-500/30 transition-all group relative";
        card.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <span class="text-xs font-bold px-2 py-1 rounded bg-slate-800 text-slate-400">${item.category}</span>
                <div class="flex gap-2">
                    ${item.video ? `<button onclick="openVideo('${item.video}')" class="text-slate-500 hover:text-red-500" title="Watch Video"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg></button>` : ''}
                    ${item.diagram ? `<button onclick="openDiagram('${item.diagram}')" class="text-slate-500 hover:text-blue-500" title="View Diagram"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg></button>` : ''}
                    <button onclick="toggleBookmark('${item.term}')" class="${isBookmarked ? 'text-pink-500' : 'text-slate-600 hover:text-pink-500'}">
                        <svg class="w-4 h-4" fill="${isBookmarked ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
                    </button>
                </div>
            </div>
            <h3 class="text-lg font-bold text-white mb-2 group-hover:text-blue-400 transition-colors">${item.term}</h3>
            <p class="text-sm text-slate-400">${item.definition}</p>
            ${item.related_terms ? `
                <div class="mt-4 pt-4 border-t border-slate-700/50 text-xs">
                    <span class="text-slate-500">Related:</span>
                    ${item.related_terms.map(t => `<button onclick="searchGlossaryTerm('${t}')" class="text-blue-400 hover:underline ml-1">${t}</button>`).join(', ')}
                </div>
            ` : ''}
        `;
        grid.appendChild(card);
    });
}

function setDailyTerm(data) {
    // Deterministic term based on day of year
    const day = Math.floor(Date.now() / 86400000);
    const term = data[day % data.length];

    document.getElementById('daily-term-title').textContent = term.term;
    document.getElementById('daily-term-def').textContent = term.definition;
    document.getElementById('daily-term-prev').textContent = term.prevention || "Knowledge is the best defense.";
}

function searchGlossaryTerm(term) {
    document.getElementById('glossary-search').value = term;
    filterGlossary(term);
    document.getElementById('glossary-search').scrollIntoView({ behavior: 'smooth' });
}

// --- Bookmarks Logic ---
function toggleBookmark(term) {
    if (bookmarks.includes(term)) {
        bookmarks = bookmarks.filter(t => t !== term);
    } else {
        bookmarks.push(term);
    }
    localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
    // Re-render
    renderGlossary(glossaryData); // To update icons
    renderBookmarks();
}

function renderBookmarks() {
    const list = document.getElementById('bookmarks-list');
    if (bookmarks.length === 0) {
        list.innerHTML = `<p class="text-slate-500 italic">No bookmarks yet.</p>`;
        return;
    }
    list.innerHTML = bookmarks.map(b => `
        <div class="flex justify-between items-center bg-slate-800 p-2 rounded">
            <span class="text-white text-sm cursor-pointer hover:text-blue-400" onclick="switchTab('education'); searchGlossaryTerm('${b}'); toggleBookmarksPanel()">${b}</span>
            <button onclick="toggleBookmark('${b}')" class="text-slate-500 hover:text-red-500">&times;</button>
        </div>
    `).join('');
}

function toggleBookmarksPanel() {
    const p = document.getElementById('bookmarks-panel');
    if (p.classList.contains('translate-x-full')) {
        p.classList.remove('translate-x-full');
    } else {
        p.classList.add('translate-x-full');
    }
}

// --- Flashcard Mode ---
function toggleFlashcardMode() {
    const container = document.getElementById('flashcard-container');
    const isHidden = container.classList.contains('hidden');

    if (isHidden) {
        container.classList.remove('hidden');
        flashcardState.terms = [...glossaryData].sort(() => Math.random() - 0.5); // Shuffle
        flashcardState.currentIndex = 0;
        updateFlashcard();
    } else {
        container.classList.add('hidden');
    }
}

function updateFlashcard() {
    const term = flashcardState.terms[flashcardState.currentIndex];
    document.getElementById('fc-term').textContent = term.term;
    document.getElementById('fc-def').textContent = term.definition;
    document.getElementById('fc-count').textContent = `${flashcardState.currentIndex + 1}/${flashcardState.terms.length}`;

    // Reset flip
    const inner = document.getElementById('flashcard-inner');
    inner.classList.remove('rotate-y-180');
    flashcardState.flipped = false;
}

function flipCard() {
    const inner = document.getElementById('flashcard-inner');
    inner.classList.toggle('rotate-y-180');
}

function nextCard() {
    if (flashcardState.currentIndex < flashcardState.terms.length - 1) {
        flashcardState.currentIndex++;
        updateFlashcard();
    }
}

function prevCard() {
    if (flashcardState.currentIndex > 0) {
        flashcardState.currentIndex--;
        updateFlashcard();
    }
}



// --- Password Tools ---
function togglePassTool(mode) {
    const checkView = document.getElementById('pass-tool-check');
    const genView = document.getElementById('pass-tool-gen');
    const btnCheck = document.getElementById('btn-pass-check');
    const btnGen = document.getElementById('btn-pass-gen');

    if (mode === 'check') {
        checkView.classList.remove('hidden');
        genView.classList.add('hidden');
        btnCheck.className = "px-3 py-1 bg-blue-600 rounded text-white";
        btnGen.className = "px-3 py-1 bg-slate-700 rounded text-slate-300 hover:text-white";
    } else {
        checkView.classList.add('hidden');
        genView.classList.remove('hidden');
        btnGen.className = "px-3 py-1 bg-green-600 rounded text-white";
        btnCheck.className = "px-3 py-1 bg-slate-700 rounded text-slate-300 hover:text-white";
    }
}

async function generatePassword() {
    const length = document.getElementById('gen-len').value;
    const useSym = document.getElementById('gen-sym').checked;
    const useNum = document.getElementById('gen-num').checked;

    try {
        const res = await fetch(`${API_BASE}/api/tools/password/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                length: parseInt(length),
                use_symbols: useSym,
                use_numbers: useNum,
                use_upper: true
            })
        });
        const data = await res.json();
        document.getElementById('gen-output').textContent = data.password;
    } catch (e) {
        alert("Generation failed");
    }
}

function copyPassword() {
    const text = document.getElementById('gen-output').textContent;
    if (text !== '...') {
        navigator.clipboard.writeText(text);
        alert("Password copied!");
    }
}


// --- Extended Tools (Stego, Exif) ---
function toggleStego(mode) {
    const hideView = document.getElementById('stego-hide');
    const extView = document.getElementById('stego-extract');
    const btnHide = document.getElementById('btn-stego-hide');
    const btnExt = document.getElementById('btn-stego-ext');

    if (mode === 'hide') {
        hideView.classList.remove('hidden');
        extView.classList.add('hidden');
        btnHide.className = "flex-1 py-1 bg-blue-600 rounded text-white";
        btnExt.className = "flex-1 py-1 bg-slate-700 rounded text-slate-300";
    } else {
        hideView.classList.add('hidden');
        extView.classList.remove('hidden');
        btnExt.className = "flex-1 py-1 bg-purple-600 rounded text-white";
        btnHide.className = "flex-1 py-1 bg-slate-700 rounded text-slate-300";
    }
}

async function hideStego() {
    const file = document.getElementById('stego-input-hide').files[0];
    const text = document.getElementById('stego-text').value;

    if (!file || !text) return alert("Please select an image and enter text.");

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(`${API_BASE}/api/tools/stego/hide?text=${encodeURIComponent(text)}`, {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error("Encoding failed");

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "secret_image.png";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    } catch (e) {
        alert(e.message);
    }
}

async function extractStego() {
    const file = document.getElementById('stego-input-ext').files[0];
    if (!file) return alert("Select an image first.");

    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch(`${API_BASE}/api/tools/stego/extract`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        document.getElementById('stego-result').textContent = data.text;
    } catch (e) {
        document.getElementById('stego-result').textContent = "Extraction failed.";
    }
}

async function viewExif() {
    const file = document.getElementById('exif-input').files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const container = document.getElementById('exif-result');
    container.innerHTML = '<p class="text-slate-500 text-center mt-4">Extracting metadata...</p>';

    try {
        const res = await fetch(`${API_BASE}/api/tools/exif`, {
            method: 'POST',
            body: formData
        });
        if (!res.ok) throw new Error(`Server returned ${res.status}`);
        const data = await res.json();

        if (data.status) {
            const isError = data.status.toLowerCase().includes('error');
            const color = isError ? 'text-red-400' : 'text-slate-500';
            container.innerHTML = `<p class="${color} text-center mt-10">${data.status}</p>`;
            return;
        }

        if (Object.keys(data).length === 0) {
            container.innerHTML = '<p class="text-slate-500 text-center mt-10">No EXIF metadata found.</p>';
            return;
        }

        let html = '<table class="w-full text-sm text-left"><tbody class="divide-y divide-slate-700">';
        for (const [key, val] of Object.entries(data)) {
            // Filter huge binary dumps
            const displayVal = (typeof val === 'string' && val.length > 50) ? val.substring(0, 50) + '...' : val;
            html += `
                <tr>
                    <td class="py-2 text-slate-400 font-mono text-xs w-1/3">${key}</td>
                    <td class="py-2 text-white break-all">${displayVal}</td>
                </tr>
             `;
        }
        html += '</tbody></table>';
        container.innerHTML = html;

    } catch (e) {
        console.error("Exif Error:", e);
        container.innerHTML = `<p class="text-red-400 text-center">Extraction failed: ${e.message}</p>`;
    }
}

// --- News Feed ---
async function loadNews() {
    const feed = document.getElementById('news-feed');
    if (!feed) return;

    // Debug indicator
    feed.innerHTML = '<p class="text-slate-500 text-sm animate-pulse">Contacting server...</p>';

    try {
        const res = await fetch(`${API_BASE}/api/news`);
        if (!res.ok) throw new Error(`Server returned ${res.status}`);

        const news = await res.json();

        if (news.length === 0) {
            feed.innerHTML = '<p class="text-slate-500 text-sm">No recent news available.</p>';
            return;
        }

        feed.innerHTML = news.map(item => `
            <div class="border-l-2 border-purple-500 pl-3 py-1 hover:bg-slate-800/50 transition-colors">
                <a href="${item.link}" target="_blank" class="text-white hover:text-purple-400 font-medium text-sm block mb-1 line-clamp-1">${item.title}</a>
                <div class="flex justify-between text-xs text-slate-500">
                    <span>${item.source}</span>
                    <span>${item.published}</span>
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error("News Load Error:", e);
        feed.innerHTML = `<p class="text-red-400 text-sm">Error: ${e.message}. Check backend console.</p>`;
    }
}

// --- Modals ---
function openVideo(url) {
    document.getElementById('video-frame').src = url;
    document.getElementById('video-modal').classList.remove('hidden');
}

function openDiagram(name) {
    const path = `diagrams/${name}.svg`; // Assuming we serve diagrams from here or static
    // Actually we need to make sure diagrams are reachable. 
    // They are in frontend/diagrams. Static mount is on frontend so /app/diagrams/name.svg
    document.getElementById('diagram-img').src = `diagrams/${name}.svg`;
    document.getElementById('diagram-modal').classList.remove('hidden');
}

function closeModal(id) {
    document.getElementById(id).classList.add('hidden');
    if (id === 'video-modal') {
        document.getElementById('video-frame').src = ''; // Stop video
    }
}
 
 / /   - - -   P e r s o n a l   S e c u r i t y   L o g i c   - - -  
  
 l e t   s c a m T r e e   =   { } ;  
 l e t   c u r r e n t S c a m S t e p   =   n u l l ;  
  
 a s y n c   f u n c t i o n   l o a d P e r s o n a l S e c u r i t y ( )   {  
         / /   L o a d   d a t a   f o r   v a r i o u s   s e c t i o n s   i f   n e e d e d  
         / /   D e c l u t t e r   g u i d e   i s   s i m p l e   l i s t  
         l o a d D e c l u t t e r ( ) ;  
 }  
  
 / /   1 .   P r i v a c y   C h e c k l i s t s  
 a s y n c   f u n c t i o n   o p e n C h e c k l i s t ( p l a t f o r m )   {  
         c o n s t   r e s   =   a w a i t   f e t c h ( ` $ { A P I _ B A S E } / a p i / p e r s o n a l / c h o i c e s ` ) ;  
         c o n s t   d a t a   =   a w a i t   r e s . j s o n ( ) ;  
         c o n s t   l i s t   =   d a t a [ p l a t f o r m ] ;  
  
         d o c u m e n t . g e t E l e m e n t B y I d ( ' c h e c k l i s t - t i t l e ' ) . i n n e r H T M L   =   `  
                 < s p a n   c l a s s = " c a p i t a l i z e " > $ { p l a t f o r m } < / s p a n >   P r i v a c y   C h e c k l i s t  
         ` ;  
  
         c o n s t   c o n t a i n e r   =   d o c u m e n t . g e t E l e m e n t B y I d ( ' c h e c k l i s t - s t e p s ' ) ;  
         c o n t a i n e r . i n n e r H T M L   =   l i s t . m a p ( i t e m   = >   `  
                 < d i v   c l a s s = " f l e x   i t e m s - s t a r t   g a p - 3   p - 3   b g - s l a t e - 8 0 0 / 5 0   r o u n d e d   b o r d e r   b o r d e r - s l a t e - 7 0 0 " >  
                         < i n p u t   t y p e = " c h e c k b o x "   i d = " $ { i t e m . i d } "   o n c h a n g e = " s a v e C h e c k l i s t ( ' $ { p l a t f o r m } ' ,   ' $ { i t e m . i d } ' ) "    
                                 c l a s s = " m t - 1   w - 5   h - 5   r o u n d e d   b o r d e r - s l a t e - 6 0 0   b g - s l a t e - 7 0 0   t e x t - b l u e - 6 0 0   f o c u s : r i n g - b l u e - 6 0 0 " >  
                         < d i v >  
                                 < l a b e l   f o r = " $ { i t e m . i d } "   c l a s s = " t e x t - w h i t e   f o n t - m e d i u m   b l o c k   c u r s o r - p o i n t e r " > $ { i t e m . t e x t } < / l a b e l >  
                                 < p   c l a s s = " t e x t - s m   t e x t - s l a t e - 4 0 0 " > $ { i t e m . d e s c } < / p >  
                         < / d i v >  
                 < / d i v >  
         ` ) . j o i n ( ' ' ) ;  
  
         / /   R e s t o r e   s t a t e  
         c o n s t   s a v e d   =   J S O N . p a r s e ( l o c a l S t o r a g e . g e t I t e m ( ' p r i v a c y _ c h e c k s ' )   | |   ' { } ' ) ;  
         l i s t . f o r E a c h ( i t e m   = >   {  
                 i f   ( s a v e d [ i t e m . i d ] )   d o c u m e n t . g e t E l e m e n t B y I d ( i t e m . i d ) . c h e c k e d   =   t r u e ;  
         } ) ;  
  
         d o c u m e n t . g e t E l e m e n t B y I d ( ' c h e c k l i s t - m o d a l ' ) . c l a s s L i s t . r e m o v e ( ' h i d d e n ' ) ;  
 }  
  
 f u n c t i o n   c l o s e C h e c k l i s t ( )   {  
         d o c u m e n t . g e t E l e m e n t B y I d ( ' c h e c k l i s t - m o d a l ' ) . c l a s s L i s t . a d d ( ' h i d d e n ' ) ;  
 }  
  
 f u n c t i o n   s a v e C h e c k l i s t ( p l a t f o r m ,   i d )   {  
         c o n s t   s a v e d   =   J S O N . p a r s e ( l o c a l S t o r a g e . g e t I t e m ( ' p r i v a c y _ c h e c k s ' )   | |   ' { } ' ) ;  
         s a v e d [ i d ]   =   d o c u m e n t . g e t E l e m e n t B y I d ( i d ) . c h e c k e d ;  
         l o c a l S t o r a g e . s e t I t e m ( ' p r i v a c y _ c h e c k s ' ,   J S O N . s t r i n g i f y ( s a v e d ) ) ;  
 }  
  
 / /   2 .   S c a m   W i z a r d  
 a s y n c   f u n c t i o n   s t a r t S c a m W i z a r d ( )   {  
         c o n s t   r e s   =   a w a i t   f e t c h ( ` $ { A P I _ B A S E } / a p i / p e r s o n a l / s c a m - t r e e ` ) ;  
         s c a m T r e e   =   a w a i t   r e s . j s o n ( ) ;  
         r e n d e r S c a m S t e p ( ' s t a r t ' ) ;  
 }  
  
 f u n c t i o n   r e n d e r S c a m S t e p ( s t e p K e y )   {  
         c o n s t   s t e p   =   s c a m T r e e [ s t e p K e y ] ;  
         i f   ( ! s t e p )   r e t u r n ;  
  
         c o n s t   c o n t a i n e r   =   d o c u m e n t . g e t E l e m e n t B y I d ( ' s c a m - w i z a r d ' ) ;  
  
         / /   R e s u l t   L e a f  
         i f   ( s t e p . i s _ f i n a l )   {  
                 c o n s t   i s S a f e   =   s t e p . r e s u l t . i n c l u d e s ( ' S A F E ' ) ;  
                 c o n s t   c o l o r   =   i s S a f e   ?   ' t e x t - g r e e n - 4 0 0 '   :   ' t e x t - r e d - 4 0 0 ' ;  
                 c o n s t   b o r d e r   =   i s S a f e   ?   ' b o r d e r - g r e e n - 5 0 0 '   :   ' b o r d e r - r e d - 5 0 0 ' ;  
  
                 c o n t a i n e r . i n n e r H T M L   =   `  
                         < d i v   c l a s s = " a n i m a t e - f a d e - i n   p - 4   b o r d e r - 2   $ { b o r d e r }   r o u n d e d - x l   b g - s l a t e - 9 0 0 / 8 0 " >  
                                 < h 3   c l a s s = " t e x t - 2 x l   f o n t - b o l d   $ { c o l o r }   m b - 2 " > $ { s t e p . r e s u l t } < / h 3 >  
                                 < p   c l a s s = " t e x t - w h i t e   m b - 4 " > $ { s t e p . a d v i c e } < / p >  
                                 < b u t t o n   o n c l i c k = " s t a r t S c a m W i z a r d ( ) "   c l a s s = " t e x t - s m   t e x t - s l a t e - 4 0 0   u n d e r l i n e " > S t a r t   O v e r < / b u t t o n >  
                         < / d i v >  
                 ` ;  
                 r e t u r n ;  
         }  
  
         / /   Q u e s t i o n   N o d e  
         c o n t a i n e r . i n n e r H T M L   =   `  
                 < d i v   c l a s s = " a n i m a t e - f a d e - i n   w - f u l l   t e x t - l e f t " >  
                         < h 4   c l a s s = " t e x t - l g   t e x t - w h i t e   f o n t - m e d i u m   m b - 6 " > $ { s t e p . q u e s t i o n } < / h 4 >  
                         < d i v   c l a s s = " s p a c e - y - 3 " >  
                                 $ { s t e p . o p t i o n s . m a p ( o p t   = >   `  
                                         < b u t t o n   o n c l i c k = " r e n d e r S c a m S t e p ( ' $ { o p t . n e x t } ' ) "    
                                                 c l a s s = " w - f u l l   t e x t - l e f t   p - 3   r o u n d e d - l g   b g - s l a t e - 7 0 0   h o v e r : b g - s l a t e - 6 0 0   t e x t - s l a t e - 2 0 0   t r a n s i t i o n - c o l o r s   f l e x   j u s t i f y - b e t w e e n   i t e m s - c e n t e r   g r o u p " >  
                                                 $ { o p t . t e x t }  
                                                 < s p a n   c l a s s = " t e x t - s l a t e - 5 0 0   g r o u p - h o v e r : t e x t - w h i t e " > â    < / s p a n >  
                                         < / b u t t o n >  
                                 ` ) . j o i n ( ' ' ) }  
                         < / d i v >  
                         $ { s t e p K e y   ! = =   ' s t a r t '   ?   ` < b u t t o n   o n c l i c k = " s t a r t S c a m W i z a r d ( ) "   c l a s s = " m t - 4   t e x t - x s   t e x t - s l a t e - 5 0 0   h o v e r : t e x t - s l a t e - 3 0 0 " > R e s t a r t < / b u t t o n > `   :   ' ' }  
                 < / d i v >  
         ` ;  
 }  
  
 / /   3 .   S y m p t o m   C h e c k e r  
 a s y n c   f u n c t i o n   c h e c k S y m p t o m s ( )   {  
         c o n s t   r e s   =   a w a i t   f e t c h ( ` $ { A P I _ B A S E } / a p i / p e r s o n a l / s y m p t o m s ` ) ;  
         c o n s t   s y m p t o m s   =   a w a i t   r e s . j s o n ( ) ;  
  
         c o n s t   l i s t   =   d o c u m e n t . g e t E l e m e n t B y I d ( ' s y m p t o m - l i s t ' ) ;  
         / /   F i r s t   r e n d e r   i f   e m p t y  
         i f   ( l i s t . c h i l d r e n . l e n g t h   <   2 )   {  
                 l i s t . i n n e r H T M L   =   s y m p t o m s . m a p ( s   = >   `  
                         < l a b e l   c l a s s = " f l e x   i t e m s - c e n t e r   g a p - 2   p - 2   h o v e r : b g - s l a t e - 8 0 0   r o u n d e d   c u r s o r - p o i n t e r " >  
                                 < i n p u t   t y p e = " c h e c k b o x "   v a l u e = " $ { s . r i s k } "   c l a s s = " s y m p t o m - c h e c k   w - 4   h - 4   r o u n d e d   b g - s l a t e - 7 0 0   b o r d e r - s l a t e - 6 0 0   t e x t - r e d - 5 0 0 " >  
                                 < s p a n   c l a s s = " t e x t - s l a t e - 3 0 0   t e x t - s m " > $ { s . s y m p t o m } < / s p a n >  
                         < / l a b e l >  
                 ` ) . j o i n ( ' ' ) ;  
                 / /   A d d   a   " C a l c u l a t e "   b u t t o n   i s   o u t s i d e ,   t h i s   j u s t   r e n d e r s   l i s t  
                 r e t u r n ;  
         }  
  
         / /   C a l c u l a t e  
         l e t   t o t a l R i s k   =   0 ;  
         d o c u m e n t . q u e r y S e l e c t o r A l l ( ' . s y m p t o m - c h e c k : c h e c k e d ' ) . f o r E a c h ( c b   = >   {  
                 t o t a l R i s k   + =   p a r s e I n t ( c b . v a l u e ) ;  
         } ) ;  
  
         c o n s t   r e s u l t D i v   =   d o c u m e n t . g e t E l e m e n t B y I d ( ' s y m p t o m - r e s u l t ' ) ;  
         r e s u l t D i v . c l a s s L i s t . r e m o v e ( ' h i d d e n ' ) ;  
  
         i f   ( t o t a l R i s k   = = =   0 )   {  
                 r e s u l t D i v . c l a s s N a m e   =   " m t - 4   p - 3   b g - s l a t e - 8 0 0   r o u n d e d   b o r d e r - l - 4   b o r d e r - g r e e n - 5 0 0   a n i m a t e - f a d e - i n " ;  
                 r e s u l t D i v . i n n e r H T M L   =   ` < s t r o n g   c l a s s = " t e x t - g r e e n - 4 0 0 " > L o w   R i s k < / s t r o n g > < p   c l a s s = " t e x t - s m   t e x t - s l a t e - 3 0 0 " > N o   m a j o r   s y m p t o m s   s e l e c t e d .   K e e p   g o o d   h y g i e n e ! < / p > ` ;  
         }   e l s e   i f   ( t o t a l R i s k   <   5 )   {  
                 r e s u l t D i v . c l a s s N a m e   =   " m t - 4   p - 3   b g - s l a t e - 8 0 0   r o u n d e d   b o r d e r - l - 4   b o r d e r - y e l l o w - 5 0 0   a n i m a t e - f a d e - i n " ;  
                 r e s u l t D i v . i n n e r H T M L   =   ` < s t r o n g   c l a s s = " t e x t - y e l l o w - 4 0 0 " > M o d e r a t e   R i s k < / s t r o n g > < p   c l a s s = " t e x t - s m   t e x t - s l a t e - 3 0 0 " > S o m e   c o n c e r n i n g   s i g n s .   R u n   a   v i r u s   s c a n   a n d   c h a n g e   p a s s w o r d s . < / p > ` ;  
         }   e l s e   {  
                 r e s u l t D i v . c l a s s N a m e   =   " m t - 4   p - 3   b g - s l a t e - 8 0 0   r o u n d e d   b o r d e r - l - 4   b o r d e r - r e d - 5 0 0   a n i m a t e - f a d e - i n " ;  
                 r e s u l t D i v . i n n e r H T M L   =   ` < s t r o n g   c l a s s = " t e x t - r e d - 4 0 0 " > H i g h   R i s k < / s t r o n g > < p   c l a s s = " t e x t - s m   t e x t - s l a t e - 3 0 0 " > M u l t i p l e   s y m p t o m s   d e t e c t e d .   D i s c o n n e c t   f r o m   i n t e r n e t ,   b a c k u p   d a t a ,   a n d   c o n s i d e r   a   f a c t o r y   r e s e t . < / p > ` ;  
         }  
 }  
  
 / /   4 .   D i g i t a l   D e c l u t t e r  
 a s y n c   f u n c t i o n   l o a d D e c l u t t e r ( )   {  
         c o n s t   r e s   =   a w a i t   f e t c h ( ` $ { A P I _ B A S E } / a p i / p e r s o n a l / d e c l u t t e r ` ) ;  
         c o n s t   s t e p s   =   a w a i t   r e s . j s o n ( ) ;  
  
         c o n s t   c o n t a i n e r   =   d o c u m e n t . g e t E l e m e n t B y I d ( ' d e c l u t t e r - l i s t ' ) ;  
         c o n s t   m a t c h e s   =   d o c u m e n t . c o o k i e . m a t c h ( / d e c l u t t e r _ p r o g r e s s = ( [ ^ ; ] + ) / ) ;  
         c o n s t   s a v e d   =   m a t c h e s   ?   J S O N . p a r s e ( d e c o d e U R I C o m p o n e n t ( m a t c h e s [ 1 ] ) )   :   [ ] ;  
  
         c o n t a i n e r . i n n e r H T M L   =   s t e p s . m a p ( ( s t e p ,   i d x )   = >   {  
                 c o n s t   i s D o n e   =   s a v e d . i n c l u d e s ( i d x ) ;  
                 r e t u r n   `  
                 < d i v   c l a s s = " r e l a t i v e   p l - 6   p b - 6   b o r d e r - l - 2   $ { i s D o n e   ?   ' b o r d e r - g r e e n - 5 0 0 '   :   ' b o r d e r - s l a t e - 7 0 0 ' }   l a s t : b o r d e r - 0   l a s t : p b - 0 " >  
                         < d i v   c l a s s = " a b s o l u t e   - l e f t - [ 9 p x ]   t o p - 0   w - 4   h - 4   r o u n d e d - f u l l   $ { i s D o n e   ?   ' b g - g r e e n - 5 0 0 '   :   ' b g - s l a t e - 7 0 0 ' }   a s p e c t - s q u a r e " > < / d i v >  
                         < h 4   c l a s s = " t e x t - w h i t e   f o n t - b o l d   t e x t - s m   $ { i s D o n e   ?   ' l i n e - t h r o u g h   t e x t - s l a t e - 5 0 0 '   :   ' ' } " > $ { s t e p . t i t l e } < / h 4 >  
                         < p   c l a s s = " t e x t - x s   t e x t - s l a t e - 4 0 0   m t - 1   m b - 2 " > $ { s t e p . d e s c } < / p >  
                         < b u t t o n   o n c l i c k = " t o g g l e D e c l u t t e r ( $ { i d x } ) "   c l a s s = " t e x t - x s   p x - 2   p y - 1   r o u n d e d   $ { i s D o n e   ?   ' b g - s l a t e - 7 0 0   t e x t - s l a t e - 4 0 0 '   :   ' b g - b l u e - 6 0 0   t e x t - w h i t e ' } " >  
                                 $ { i s D o n e   ?   ' U n d o '   :   ' M a r k   D o n e ' }  
                         < / b u t t o n >  
                 < / d i v >  
         ` } ) . j o i n ( ' ' ) ;  
 }  
  
 f u n c t i o n   t o g g l e D e c l u t t e r ( i d x )   {  
         c o n s t   m a t c h e s   =   d o c u m e n t . c o o k i e . m a t c h ( / d e c l u t t e r _ p r o g r e s s = ( [ ^ ; ] + ) / ) ;  
         l e t   s a v e d   =   m a t c h e s   ?   J S O N . p a r s e ( d e c o d e U R I C o m p o n e n t ( m a t c h e s [ 1 ] ) )   :   [ ] ;  
  
         i f   ( s a v e d . i n c l u d e s ( i d x ) )   {  
                 s a v e d   =   s a v e d . f i l t e r ( i   = >   i   ! = =   i d x ) ;  
         }   e l s e   {  
                 s a v e d . p u s h ( i d x ) ;  
         }  
  
         d o c u m e n t . c o o k i e   =   ` d e c l u t t e r _ p r o g r e s s = $ { e n c o d e U R I C o m p o n e n t ( J S O N . s t r i n g i f y ( s a v e d ) ) } ;   m a x - a g e = 3 1 5 3 6 0 0 0 ;   p a t h = / ` ;  
         l o a d D e c l u t t e r ( ) ;   / /   R e - r e n d e r  
 }  
 