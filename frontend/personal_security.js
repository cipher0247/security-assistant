// --- Personal Security Logic ---

let scamTree = {};
let currentScamStep = null;

async function loadPersonalSecurity() {
    // Load data for various sections if needed
    // Declutter guide is simple list
    loadDeclutter();
    loadSymptoms();
}

// 1. Privacy Checklists
async function openChecklist(platform) {
    const res = await fetch(`${API_BASE}/api/personal/choices`);
    const data = await res.json();
    const list = data[platform];

    document.getElementById('checklist-title').innerHTML = `
        <span class="capitalize">${platform}</span> Privacy Checklist
    `;

    const container = document.getElementById('checklist-steps');
    container.innerHTML = list.map(item => `
        <div class="flex items-start gap-3 p-3 bg-slate-800/50 rounded border border-slate-700">
            <input type="checkbox" id="${item.id}" onchange="saveChecklist('${platform}', '${item.id}')" 
                class="mt-1 w-5 h-5 rounded border-slate-600 bg-slate-700 text-blue-600 focus:ring-blue-600">
            <div>
                <label for="${item.id}" class="text-white font-medium block cursor-pointer">${item.text}</label>
                <p class="text-sm text-slate-400">${item.desc}</p>
            </div>
        </div>
    `).join('');

    // Restore state
    const saved = JSON.parse(localStorage.getItem('privacy_checks') || '{}');
    list.forEach(item => {
        if (saved[item.id]) document.getElementById(item.id).checked = true;
    });

    document.getElementById('checklist-modal').classList.remove('hidden');
}

function closeChecklist() {
    document.getElementById('checklist-modal').classList.add('hidden');
}

function saveChecklist(platform, id) {
    const saved = JSON.parse(localStorage.getItem('privacy_checks') || '{}');
    saved[id] = document.getElementById(id).checked;
    localStorage.setItem('privacy_checks', JSON.stringify(saved));
}

// 2. Scam Wizard
async function startScamWizard() {
    const res = await fetch(`${API_BASE}/api/personal/scam-tree`);
    scamTree = await res.json();
    renderScamStep('start');
}

function renderScamStep(stepKey) {
    const step = scamTree[stepKey];
    if (!step) return;

    const container = document.getElementById('scam-wizard');

    // Result Leaf
    if (step.is_final) {
        const isSafe = step.result.includes('SAFE');
        const color = isSafe ? 'text-green-400' : 'text-red-400';
        const border = isSafe ? 'border-green-500' : 'border-red-500';

        container.innerHTML = `
            <div class="animate-fade-in p-4 border-2 ${border} rounded-xl bg-slate-900/80">
                <h3 class="text-2xl font-bold ${color} mb-2">${step.result}</h3>
                <p class="text-white mb-4">${step.advice}</p>
                <button onclick="startScamWizard()" class="text-sm text-slate-400 underline">Start Over</button>
            </div>
        `;
        return;
    }

    // Question Node
    container.innerHTML = `
        <div class="animate-fade-in w-full text-left">
            <h4 class="text-lg text-white font-medium mb-6">${step.question}</h4>
            <div class="space-y-3">
                ${step.options.map(opt => `
                    <button onclick="renderScamStep('${opt.next}')" 
                        class="w-full text-left p-3 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors flex justify-between items-center group">
                        ${opt.text}
                        <span class="text-slate-500 group-hover:text-white">→</span>
                    </button>
                `).join('')}
            </div>
            ${stepKey !== 'start' ? `<button onclick="startScamWizard()" class="mt-4 text-xs text-slate-500 hover:text-slate-300">Restart</button>` : ''}
        </div>
    `;
}

// 3. Symptom Checker
let userSymptoms = [];

async function loadSymptoms() {
    const list = document.getElementById('symptom-list');
    if (list.children.length > 1) return;

    try {
        const res = await fetch(`${API_BASE}/api/personal/symptoms`);
        const symptoms = await res.json();

        list.innerHTML = symptoms.map(s => `
            <label class="flex items-center gap-2 p-2 hover:bg-slate-800 rounded cursor-pointer transition-colors block w-full text-left">
                <input type="checkbox" value="${s.risk}" class="symptom-check w-4 h-4 rounded bg-slate-700 border-slate-600 text-red-500 focus:ring-red-500">
                <span class="text-slate-300 text-sm flex-1">${s.symptom}</span>
            </label>
        `).join('');
    } catch (e) {
        console.error(e);
    }
}

async function checkSymptoms() {
    // Calculate
    let totalRisk = 0;
    document.querySelectorAll('.symptom-check:checked').forEach(cb => {
        totalRisk += parseInt(cb.value);
    });

    const resultDiv = document.getElementById('symptom-result');
    resultDiv.classList.remove('hidden');

    if (totalRisk === 0) {
        resultDiv.className = "mt-4 p-3 bg-slate-800 rounded border-l-4 border-green-500 animate-fade-in";
        resultDiv.innerHTML = `<strong class="text-green-400">Low Risk</strong><p class="text-sm text-slate-300">No major symptoms selected. Keep good hygiene!</p>`;
    } else if (totalRisk < 5) {
        resultDiv.className = "mt-4 p-3 bg-slate-800 rounded border-l-4 border-yellow-500 animate-fade-in";
        resultDiv.innerHTML = `<strong class="text-yellow-400">Moderate Risk</strong><p class="text-sm text-slate-300">Some concerning signs. Run a virus scan and change passwords.</p>`;
    } else {
        resultDiv.className = "mt-4 p-3 bg-slate-800 rounded border-l-4 border-red-500 animate-fade-in";
        resultDiv.innerHTML = `<strong class="text-red-400">High Risk</strong><p class="text-sm text-slate-300">Multiple symptoms detected. Disconnect from internet, backup data, and consider a factory reset.</p>`;
    }
}

// 4. Digital Declutter
async function loadDeclutter() {
    const res = await fetch(`${API_BASE}/api/personal/declutter`);
    const steps = await res.json();

    const container = document.getElementById('declutter-list');
    const matches = document.cookie.match(/declutter_progress=([^;]+)/);
    const saved = matches ? JSON.parse(decodeURIComponent(matches[1])) : [];

    container.innerHTML = steps.map((step, idx) => {
        const isDone = saved.includes(idx);
        return `
        <div class="relative pl-6 pb-6 border-l-2 ${isDone ? 'border-green-500' : 'border-slate-700'} last:border-0 last:pb-0">
            <div class="absolute -left-[9px] top-0 w-4 h-4 rounded-full ${isDone ? 'bg-green-500' : 'bg-slate-700'} aspect-square"></div>
            <h4 class="text-white font-bold text-sm ${isDone ? 'line-through text-slate-500' : ''}">${step.title}</h4>
            <p class="text-xs text-slate-400 mt-1 mb-2">${step.desc}</p>
            <button onclick="toggleDeclutter(${idx})" class="text-xs px-2 py-1 rounded ${isDone ? 'bg-slate-700 text-slate-400' : 'bg-blue-600 text-white'}">
                ${isDone ? 'Undo' : 'Mark Done'}
            </button>
        </div>
    `}).join('');
}

function toggleDeclutter(idx) {
    const matches = document.cookie.match(/declutter_progress=([^;]+)/);
    let saved = matches ? JSON.parse(decodeURIComponent(matches[1])) : [];

    if (saved.includes(idx)) {
        saved = saved.filter(i => i !== idx);
    } else {
        saved.push(idx);
    }

    document.cookie = `declutter_progress=${encodeURIComponent(JSON.stringify(saved))}; max-age=31536000; path=/`;
    loadDeclutter(); // Re-render
}

// 5. Deepfake Detector UI
function openDeepfakeTool() {
    document.getElementById('deepfake-modal').classList.remove('hidden');
    // Reset state
    document.getElementById('deepfake-upload').classList.remove('hidden');
    document.getElementById('deepfake-loading').classList.add('hidden');
    document.getElementById('deepfake-result').classList.add('hidden');
    document.getElementById('deepfake-input').value = '';
}

async function analyzeDeepfake() {
    const input = document.getElementById('deepfake-input');
    if (!input.files || !input.files[0]) return;

    const file = input.files[0];
    const isVideo = file.type.startsWith('video/');

    // Show loading
    document.getElementById('deepfake-upload').classList.add('hidden');
    document.getElementById('deepfake-loading').classList.remove('hidden');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch(`${API_BASE}/api/scan/deepfake`, {
            method: 'POST',
            body: formData
        });

        if (!res.ok) throw new Error('Analysis failed');

        const data = await res.json();
        const result = data.result;

        document.getElementById('deepfake-loading').classList.add('hidden');
        document.getElementById('deepfake-result').classList.remove('hidden');

        const originalImg = document.getElementById('deepfake-original-img');
        const originalVideo = document.getElementById('deepfake-original-video');
        const elaImg = document.getElementById('deepfake-ela-img');
        const riskPanel = document.getElementById('deepfake-risk-panel');

        if (isVideo) {
            originalImg.classList.add('hidden');
            originalVideo.classList.remove('hidden');
            originalVideo.src = URL.createObjectURL(file);

            // Show first frame ELA or placeholder
            if (result.frames && result.frames.length > 0) {
                elaImg.src = result.frames[1].ela_image || result.frames[0].ela_image;
            }

            document.getElementById('deepfake-frames-container').classList.remove('hidden');
            document.getElementById('deepfake-frames-grid').innerHTML = result.frames.map((f, i) => `
                <div class="min-w-[150px] aspect-video bg-slate-800 rounded border border-slate-700 overflow-hidden relative group cursor-pointer"
                    onclick="document.getElementById('deepfake-ela-img').src = '${f.ela_image}'">
                    <img src="${f.ela_image}" class="w-full h-full object-cover">
                    <div class="absolute bottom-0 left-0 bg-black/60 text-white text-[10px] px-1">Score: ${f.score}</div>
                </div>
            `).join('');
        } else {
            originalVideo.classList.add('hidden');
            originalImg.classList.remove('hidden');
            const url = URL.createObjectURL(file);
            originalImg.src = url;

            elaImg.style.filter = "none"; // Remove mock filter
            elaImg.src = result.ela_image;

            document.getElementById('deepfake-frames-container').classList.add('hidden');
        }

        // Result Panel
        const score = result.score;
        let riskColor = 'text-green-400';
        let riskText = 'Likely Original';
        let riskIcon = 'ok';

        if (score > 60) {
            riskColor = 'text-red-400';
            riskText = 'Potential Deepfake';
            riskIcon = 'warn';
        } else if (score > 30) {
            riskColor = 'text-yellow-400';
            riskText = 'Suspicious';
            riskIcon = 'warn';
        }

        riskPanel.innerHTML = `
            <div>
                <h3 class="text-2xl font-bold ${riskColor} mb-1">${riskText}</h3>
                <p class="text-slate-400">Error Level Analysis complete. Score based on artifact variance.</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="text-right">
                    <p class="text-xs text-slate-400 uppercase tracking-wider">Suspicion Score</p>
                    <p class="text-3xl font-bold ${riskColor}">${score}%</p>
                </div>
                <div class="w-16 h-16 rounded-full border-4 ${score > 50 ? 'border-red-500' : 'border-green-500'} flex items-center justify-center bg-slate-800">
                    <span class="text-2xl">${score > 50 ? 'âš ï¸ ' : 'âœ…'}</span>
                </div>
            </div>
        `;
    } catch (e) {
        console.error(e);
        document.getElementById('deepfake-loading').classList.add('hidden');
        element = document.getElementById('deepfake-upload');
        element.classList.remove('hidden');
        alert("Analysis failed. Please try a valid image/video file.");
    }
}
