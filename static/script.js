// ===== State Management =====
const state = {
    selectedEngine: 'edge-tts',
    selectedVoice: null,
    allVoices: [],
    filteredVoices: [],
    resultAudioBlob: null,
    referenceAudio: null,
    coquiAudio: null,
    emotionAudio: null,
    emotionMode: 'none',
    emotionVector: [0, 0, 0, 0, 0, 0, 0, 0], // [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
    indexTtsAvailable: false,
    coquiTtsAvailable: false
};

// ===== DOM Elements =====
const elements = {
    // Engine selection
    edgeTtsBtn: document.getElementById('edgeTtsBtn'),
    indexTtsBtn: document.getElementById('indexTtsBtn'),
    coquiTtsBtn: document.getElementById('coquiTtsBtn'),
    indexTtsStatus: document.getElementById('indexTtsStatus'),
    coquiTtsStatus: document.getElementById('coquiTtsStatus'),
    edgeTtsSection: document.getElementById('edgeTtsSection'),
    indexTtsSection: document.getElementById('indexTtsSection'),
    coquiTtsSection: document.getElementById('coquiTtsSection'),

    // Voice selection (Edge-TTS)
    voiceGrid: document.getElementById('voiceGrid'),
    voiceSearch: document.getElementById('voiceSearch'),
    languageFilter: document.getElementById('languageFilter'),
    genderFilter: document.getElementById('genderFilter'),
    selectedVoiceDisplay: document.getElementById('selectedVoiceDisplay'),
    selectedVoiceName: document.getElementById('selectedVoiceName'),
    selectedVoiceLocale: document.getElementById('selectedVoiceLocale'),

    // Reference audio upload (Index-TTS2)
    referenceUploadArea: document.getElementById('referenceUploadArea'),
    referenceAudioInput: document.getElementById('referenceAudioInput'),
    uploadPlaceholder: document.getElementById('uploadPlaceholder'),
    uploadPreview: document.getElementById('uploadPreview'),
    previewName: document.getElementById('previewName'),
    referencePreview: document.getElementById('referencePreview'),
    removeReference: document.getElementById('removeReference'),

    // Coqui TTS upload
    coquiUploadArea: document.getElementById('coquiUploadArea'),
    coquiAudioInput: document.getElementById('coquiAudioInput'),
    coquiUploadPlaceholder: document.getElementById('coquiUploadPlaceholder'),
    coquiUploadPreview: document.getElementById('coquiUploadPreview'),
    coquiPreviewName: document.getElementById('coquiPreviewName'),
    coquiReferencePreview: document.getElementById('coquiReferencePreview'),
    removeCoquiReference: document.getElementById('removeCoquiReference'),
    coquiLanguageSelect: document.getElementById('coquiLanguageSelect'),

    // Emotion control
    emotionControl: document.getElementById('emotionControl'),
    emotionTabs: document.querySelectorAll('.emotion-tab'),
    emotionAudioMode: document.getElementById('emotionAudioMode'),
    emotionManualMode: document.getElementById('emotionManualMode'),
    emotionUploadArea: document.getElementById('emotionUploadArea'),
    emotionAudioInput: document.getElementById('emotionAudioInput'),
    emotionUploadPreview: document.getElementById('emotionUploadPreview'),
    emotionPreviewName: document.getElementById('emotionPreviewName'),
    emotionPreview: document.getElementById('emotionPreview'),
    removeEmotion: document.getElementById('removeEmotion'),
    emotionIntensity: document.getElementById('emotionIntensity'),
    emotionIntensityValue: document.getElementById('emotionIntensityValue'),
    emotionRanges: document.querySelectorAll('.emotion-range'),

    // Text input
    textInput: document.getElementById('textInput'),
    charCount: document.getElementById('charCount'),
    convertBtn: document.getElementById('convertBtn'),

    // Results
    resultsSection: document.getElementById('resultsSection'),
    resultAudio: document.getElementById('resultAudio'),
    downloadBtn: document.getElementById('downloadBtn'),

    // UI feedback
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingText: document.getElementById('loadingText'),
    notification: document.getElementById('notification'),
    notificationIcon: document.getElementById('notificationIcon'),
    notificationText: document.getElementById('notificationText')
};

// ===== Utility Functions =====
function showNotification(message, type = 'success') {
    elements.notification.className = 'notification show ' + type;
    elements.notificationIcon.textContent = type === 'success' ? '✓' : '✕';
    elements.notificationText.textContent = message;

    setTimeout(() => {
        elements.notification.classList.remove('show');
    }, 4000);
}

function showLoading(message = 'Processing...') {
    elements.loadingText.textContent = message;
    elements.loadingOverlay.classList.add('active');
}

function hideLoading() {
    elements.loadingOverlay.classList.remove('active');
}

// ===== Engine Management =====
async function checkEngines() {
    try {
        const response = await fetch('/api/engines');
        if (!response.ok) throw new Error('Failed to check engines');

        const data = await response.json();
        const indexEngine = data.engines.find(e => e.id === 'index-tts2');
        const coquiEngine = data.engines.find(e => e.id === 'coqui-tts');

        state.indexTtsAvailable = indexEngine?.available || false;
        state.coquiTtsAvailable = coquiEngine?.available || false;

        // Update Index-TTS UI
        if (state.indexTtsAvailable) {
            elements.indexTtsStatus.innerHTML = '<span class="status-badge success">✓ Ready</span>';
            elements.indexTtsBtn.disabled = false;
        } else {
            // Check if we're in a deployed environment
            const isDeployed = window.location.hostname !== 'localhost' &&
                window.location.hostname !== '127.0.0.1';

            if (isDeployed) {
                elements.indexTtsStatus.innerHTML = '<span class="status-badge warning">⚠ Models Loading...</span>';
            } else {
                elements.indexTtsStatus.innerHTML = '<span class="status-badge warning">⚠ Deploy to Enable</span>';
            }
            elements.indexTtsBtn.disabled = false; // Still allow clicking to show message
        }

        // Update Coqui-TTS UI
        if (state.coquiTtsAvailable) {
            elements.coquiTtsStatus.innerHTML = '<span class="status-badge success">✓ Ready</span>';
            elements.coquiTtsBtn.disabled = false;
        } else {
            // Check if we're in a deployed environment
            const isDeployed = window.location.hostname !== 'localhost' &&
                window.location.hostname !== '127.0.0.1';

            if (isDeployed) {
                elements.coquiTtsStatus.innerHTML = '<span class="status-badge warning">⚠ Models Loading...</span>';
            } else {
                elements.coquiTtsStatus.innerHTML = '<span class="status-badge warning">⚠ Deploy to Enable</span>';
            }
            elements.coquiTtsBtn.disabled = false; // Still allow clicking to show message
        }

    } catch (error) {
        console.error('Error checking engines:', error);
        elements.indexTtsStatus.innerHTML = '<span class="status-badge error">✕ Error</span>';
        elements.coquiTtsStatus.innerHTML = '<span class="status-badge error">✕ Error</span>';
    }
}

function switchEngine(engineId) {
    state.selectedEngine = engineId;

    // Update button states
    document.querySelectorAll('.engine-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.engine === engineId);
    });

    // Show/hide appropriate sections
    if (engineId === 'edge-tts') {
        elements.edgeTtsSection.style.display = 'block';
        elements.indexTtsSection.style.display = 'none';
        if (elements.coquiTtsSection) elements.coquiTtsSection.style.display = 'none';
    } else if (engineId === 'index-tts2') {
        elements.edgeTtsSection.style.display = 'none';
        elements.indexTtsSection.style.display = 'block';
        if (elements.coquiTtsSection) elements.coquiTtsSection.style.display = 'none';

        if (!state.indexTtsAvailable) {
            const isDeployed = window.location.hostname !== 'localhost' &&
                window.location.hostname !== '127.0.0.1';

            if (isDeployed) {
                showNotification('Index-TTS2 models are being downloaded. This may take a few minutes on first deployment.', 'warning');
            } else {
                showNotification('Index-TTS2 will be automatically set up when you deploy to Render. Models download during build (~10-15 min).', 'info');
            }
        }
    } else if (engineId === 'coqui-tts') {
        elements.edgeTtsSection.style.display = 'none';
        elements.indexTtsSection.style.display = 'none';
        if (elements.coquiTtsSection) elements.coquiTtsSection.style.display = 'block';

        if (!state.coquiTtsAvailable) {
            const isDeployed = window.location.hostname !== 'localhost' &&
                window.location.hostname !== '127.0.0.1';

            if (isDeployed) {
                showNotification('Coqui TTS models are being downloaded. This may take a few minutes on first deployment.', 'warning');
            } else {
                showNotification('Coqui TTS will be automatically set up when you deploy to Render. Models download during build.', 'info');
            }
        }
    }
}

// ===== Voice Loading and Filtering (Edge-TTS) =====
async function loadVoices() {
    try {
        showLoading('Loading voices...');

        const response = await fetch('/api/voices');
        if (!response.ok) throw new Error('Failed to load voices');

        const data = await response.json();
        state.allVoices = data.voices;
        state.filteredVoices = data.voices;

        // Populate language filter
        const languages = [...new Set(data.voices.map(v => v.locale))].sort();
        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang;
            option.textContent = lang;
            elements.languageFilter.appendChild(option);
        });

        // Display voices
        displayVoices(state.filteredVoices);

        // Select first English voice by default
        const defaultVoice = data.voices.find(v => v.locale.startsWith('en-US')) || data.voices[0];
        if (defaultVoice) {
            selectVoice(defaultVoice);
        }

        hideLoading();

    } catch (error) {
        hideLoading();
        showNotification('Error loading voices: ' + error.message, 'error');
        console.error('Error loading voices:', error);
    }
}

function displayVoices(voices) {
    if (voices.length === 0) {
        elements.voiceGrid.innerHTML = '<div class="loading-voices">No voices found</div>';
        return;
    }

    elements.voiceGrid.innerHTML = voices.map(voice => `
        <div class="voice-card ${state.selectedVoice?.name === voice.name ? 'selected' : ''}" 
             data-voice-name="${voice.name}">
            <div class="voice-card-name">${voice.display_name.split(' - ')[0]}</div>
            <div class="voice-card-locale">${voice.locale}</div>
            <div class="voice-card-gender">${voice.gender}</div>
        </div>
    `).join('');

    // Add click handlers
    document.querySelectorAll('.voice-card').forEach(card => {
        card.addEventListener('click', () => {
            const voiceName = card.dataset.voiceName;
            const voice = state.allVoices.find(v => v.name === voiceName);
            if (voice) selectVoice(voice);
        });
    });
}

function selectVoice(voice) {
    state.selectedVoice = voice;

    // Update selected voice display
    elements.selectedVoiceName.textContent = voice.display_name;
    elements.selectedVoiceLocale.textContent = `${voice.locale} • ${voice.gender}`;
    elements.selectedVoiceDisplay.style.display = 'block';

    // Update voice cards
    document.querySelectorAll('.voice-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.voiceName === voice.name);
    });
}

function filterVoices() {
    const searchTerm = elements.voiceSearch.value.toLowerCase();
    const languageFilter = elements.languageFilter.value;
    const genderFilter = elements.genderFilter.value;

    state.filteredVoices = state.allVoices.filter(voice => {
        const matchesSearch = voice.display_name.toLowerCase().includes(searchTerm) ||
            voice.locale.toLowerCase().includes(searchTerm);
        const matchesLanguage = !languageFilter || voice.locale === languageFilter;
        const matchesGender = !genderFilter || voice.gender === genderFilter;

        return matchesSearch && matchesLanguage && matchesGender;
    });

    displayVoices(state.filteredVoices);
}

// ===== File Upload Handlers (Index-TTS2) =====
function setupFileUpload() {
    // Reference audio upload
    elements.referenceUploadArea.addEventListener('click', () => {
        if (!state.referenceAudio) {
            elements.referenceAudioInput.click();
        }
    });

    elements.referenceUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.referenceUploadArea.classList.add('dragover');
    });

    elements.referenceUploadArea.addEventListener('dragleave', () => {
        elements.referenceUploadArea.classList.remove('dragover');
    });

    elements.referenceUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.referenceUploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleReferenceAudio(files[0]);
        }
    });

    elements.referenceAudioInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleReferenceAudio(e.target.files[0]);
        }
    });

    elements.removeReference.addEventListener('click', (e) => {
        e.stopPropagation();
        clearReferenceAudio();
    });

    // Emotion audio upload
    elements.emotionUploadArea.addEventListener('click', () => {
        if (!state.emotionAudio) {
            elements.emotionAudioInput.click();
        }
    });

    elements.emotionAudioInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleEmotionAudio(e.target.files[0]);
        }
    });

    elements.removeEmotion.addEventListener('click', (e) => {
        e.stopPropagation();
        clearEmotionAudio();
    });
}

function handleReferenceAudio(file) {
    // Validate file type
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/ogg', 'audio/flac', 'audio/x-m4a'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(wav|mp3|ogg|flac|m4a)$/i)) {
        showNotification('Invalid file type. Please upload an audio file.', 'error');
        return;
    }

    state.referenceAudio = file;

    // Update UI
    elements.uploadPlaceholder.style.display = 'none';
    elements.uploadPreview.style.display = 'block';
    elements.previewName.textContent = file.name;

    // Create audio preview
    const url = URL.createObjectURL(file);
    elements.referencePreview.src = url;

    showNotification('Reference audio uploaded successfully', 'success');
}

function clearReferenceAudio() {
    state.referenceAudio = null;
    elements.uploadPlaceholder.style.display = 'block';
    elements.uploadPreview.style.display = 'none';
    elements.referencePreview.src = '';
    elements.referenceAudioInput.value = '';
}

function handleEmotionAudio(file) {
    state.emotionAudio = file;

    // Update UI
    elements.emotionUploadArea.querySelector('.upload-placeholder').style.display = 'none';
    elements.emotionUploadPreview.style.display = 'block';
    elements.emotionPreviewName.textContent = file.name;

    // Create audio preview
    const url = URL.createObjectURL(file);
    elements.emotionPreview.src = url;

    showNotification('Emotion audio uploaded successfully', 'success');
}

function clearEmotionAudio() {
    state.emotionAudio = null;
    elements.emotionUploadArea.querySelector('.upload-placeholder').style.display = 'block';
    elements.emotionUploadPreview.style.display = 'none';
    elements.emotionPreview.src = '';
    elements.emotionAudioInput.value = '';
}

// ===== Coqui TTS File Upload Handlers =====
function setupCoquiFileUpload() {
    if (!elements.coquiUploadArea) return;

    // Coqui audio upload
    elements.coquiUploadArea.addEventListener('click', () => {
        if (!state.coquiAudio) {
            elements.coquiAudioInput.click();
        }
    });

    elements.coquiUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.coquiUploadArea.classList.add('dragover');
    });

    elements.coquiUploadArea.addEventListener('dragleave', () => {
        elements.coquiUploadArea.classList.remove('dragover');
    });

    elements.coquiUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.coquiUploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleCoquiAudio(files[0]);
        }
    });

    elements.coquiAudioInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleCoquiAudio(e.target.files[0]);
        }
    });

    elements.removeCoquiReference.addEventListener('click', (e) => {
        e.stopPropagation();
        clearCoquiAudio();
    });
}

function handleCoquiAudio(file) {
    // Validate file type
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/ogg', 'audio/flac', 'audio/x-m4a'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(wav|mp3|ogg|flac|m4a)$/i)) {
        showNotification('Invalid file type. Please upload an audio file.', 'error');
        return;
    }

    state.coquiAudio = file;

    // Update UI
    elements.coquiUploadPlaceholder.style.display = 'none';
    elements.coquiUploadPreview.style.display = 'block';
    elements.coquiPreviewName.textContent = file.name;

    // Create audio preview
    const url = URL.createObjectURL(file);
    elements.coquiReferencePreview.src = url;

    showNotification('Reference audio uploaded successfully', 'success');
}

function clearCoquiAudio() {
    state.coquiAudio = null;
    elements.coquiUploadPlaceholder.style.display = 'block';
    elements.coquiUploadPreview.style.display = 'none';
    elements.coquiReferencePreview.src = '';
    elements.coquiAudioInput.value = '';
}

// ===== Emotion Control =====
function setupEmotionControl() {
    // Emotion mode tabs
    elements.emotionTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const mode = tab.dataset.mode;
            switchEmotionMode(mode);
        });
    });

    // Emotion intensity slider
    elements.emotionIntensity.addEventListener('input', (e) => {
        elements.emotionIntensityValue.textContent = e.target.value;
    });

    // Emotion range sliders
    elements.emotionRanges.forEach(range => {
        range.addEventListener('input', (e) => {
            const emotion = e.target.dataset.emotion;
            const value = e.target.value;
            document.getElementById(`${emotion}Value`).textContent = value;

            // Update emotion vector
            const emotionIndex = ['happy', 'angry', 'sad', 'afraid', 'disgusted', 'melancholic', 'surprised', 'calm'].indexOf(emotion);
            if (emotionIndex !== -1) {
                state.emotionVector[emotionIndex] = parseFloat(value) / 100;
            }
        });
    });
}

function switchEmotionMode(mode) {
    state.emotionMode = mode;

    // Update tabs
    elements.emotionTabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.mode === mode);
    });

    // Show/hide content
    elements.emotionAudioMode.style.display = mode === 'audio' ? 'block' : 'none';
    elements.emotionManualMode.style.display = mode === 'manual' ? 'block' : 'none';
}

// ===== Text Input Handler =====
function setupTextInput() {
    elements.textInput.addEventListener('input', (e) => {
        const length = e.target.value.length;
        elements.charCount.textContent = length;
    });
}

// ===== Conversion Handlers =====
async function convertTextToSpeech() {
    if (state.selectedEngine === 'edge-tts') {
        await convertWithEdgeTTS();
    } else if (state.selectedEngine === 'index-tts2') {
        await convertWithIndexTTS();
    } else if (state.selectedEngine === 'coqui-tts') {
        await convertWithCoquiTTS();
    }
}

async function convertWithEdgeTTS() {
    // Validate inputs
    if (!state.selectedVoice) {
        showNotification('Please select a voice first', 'error');
        return;
    }

    const text = elements.textInput.value.trim();
    if (!text) {
        showNotification('Please enter some text to convert', 'error');
        return;
    }

    try {
        showLoading('Generating speech with Edge-TTS...');

        // Prepare form data
        const formData = new FormData();
        formData.append('text', text);
        formData.append('voice', state.selectedVoice.name);

        // Make API request
        const response = await fetch('/api/convert/text-to-speech', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Conversion failed');
        }

        // Get audio blob
        const blob = await response.blob();
        state.resultAudioBlob = blob;

        // Display result
        const audioUrl = URL.createObjectURL(blob);
        elements.resultAudio.src = audioUrl;
        elements.resultsSection.style.display = 'block';

        // Scroll to results
        elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        hideLoading();
        showNotification('Speech generated successfully!', 'success');

    } catch (error) {
        hideLoading();
        showNotification(error.message, 'error');
        console.error('Conversion error:', error);
    }
}

async function convertWithIndexTTS() {
    // Validate inputs
    if (!state.referenceAudio) {
        showNotification('Please upload a reference audio file', 'error');
        return;
    }

    const text = elements.textInput.value.trim();
    if (!text) {
        showNotification('Please enter some text to convert', 'error');
        return;
    }

    if (!state.indexTtsAvailable) {
        const isDeployed = window.location.hostname !== 'localhost' &&
            window.location.hostname !== '127.0.0.1';

        if (isDeployed) {
            showNotification('Index-TTS2 models are still loading. Please wait a few minutes and try again.', 'warning');
        } else {
            showNotification('Index-TTS2 will be available after deployment to Render. Use Edge-TTS for now, or deploy your app!', 'info');
        }
        return;
    }

    try {
        showLoading('Cloning voice with Index-TTS2... (this may take longer)');

        // Prepare form data
        const formData = new FormData();
        formData.append('text', text);
        formData.append('speaker_audio', state.referenceAudio);
        formData.append('emotion_mode', state.emotionMode);

        // Add emotion data based on mode
        if (state.emotionMode === 'audio' && state.emotionAudio) {
            formData.append('emotion_audio', state.emotionAudio);
            formData.append('emotion_intensity', elements.emotionIntensity.value / 100);
        } else if (state.emotionMode === 'manual') {
            formData.append('emotion_vector', JSON.stringify(state.emotionVector));
        }

        // Make API request
        const response = await fetch('/api/index-tts/synthesize-emotion', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Voice cloning failed');
        }

        // Get audio blob
        const blob = await response.blob();
        state.resultAudioBlob = blob;

        // Display result
        const audioUrl = URL.createObjectURL(blob);
        elements.resultAudio.src = audioUrl;
        elements.resultsSection.style.display = 'block';

        // Scroll to results
        elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        hideLoading();
        showNotification('Voice cloned successfully!', 'success');

    } catch (error) {
        hideLoading();
        showNotification(error.message, 'error');
        console.error('Voice cloning error:', error);
    }
}

async function convertWithCoquiTTS() {
    // Validate inputs
    if (!state.coquiAudio) {
        showNotification('Please upload a reference audio file', 'error');
        return;
    }

    const text = elements.textInput.value.trim();
    if (!text) {
        showNotification('Please enter some text to convert', 'error');
        return;
    }

    if (!state.coquiTtsAvailable) {
        const isDeployed = window.location.hostname !== 'localhost' &&
            window.location.hostname !== '127.0.0.1';

        if (isDeployed) {
            showNotification('Coqui TTS models are still loading. Please wait a few minutes and try again.', 'warning');
        } else {
            showNotification('Coqui TTS will be available after deployment to Render. Use Edge-TTS for now, or deploy your app!', 'info');
        }
        return;
    }

    try {
        showLoading('Cloning voice with Coqui TTS... (this may take longer)');

        // Prepare form data
        const formData = new FormData();
        formData.append('text', text);
        formData.append('speaker_audio', state.coquiAudio);

        // Get selected language
        const language = elements.coquiLanguageSelect ? elements.coquiLanguageSelect.value : 'en';
        formData.append('language', language);

        // Make API request
        const response = await fetch('/api/coqui/clone-voice', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Voice cloning failed');
        }

        // Get audio blob
        const blob = await response.blob();
        state.resultAudioBlob = blob;

        // Display result
        const audioUrl = URL.createObjectURL(blob);
        elements.resultAudio.src = audioUrl;
        elements.resultsSection.style.display = 'block';

        // Scroll to results
        elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        hideLoading();
        showNotification('Voice cloned successfully with Coqui TTS!', 'success');

    } catch (error) {
        hideLoading();
        showNotification(error.message, 'error');
        console.error('Coqui TTS error:', error);
    }
}

function downloadAudio() {
    if (!state.resultAudioBlob) {
        showNotification('No audio to download', 'error');
        return;
    }

    const url = URL.createObjectURL(state.resultAudioBlob);
    const a = document.createElement('a');
    a.href = url;
    const extension = state.selectedEngine === 'edge-tts' ? 'mp3' : 'wav';
    a.download = `voicemaker_${state.selectedEngine}_${Date.now()}.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Audio downloaded!', 'success');
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Engine selection
    elements.edgeTtsBtn.addEventListener('click', () => switchEngine('edge-tts'));
    elements.indexTtsBtn.addEventListener('click', () => switchEngine('index-tts2'));
    if (elements.coquiTtsBtn) {
        elements.coquiTtsBtn.addEventListener('click', () => switchEngine('coqui-tts'));
    }

    // Voice search and filters (Edge-TTS)
    elements.voiceSearch.addEventListener('input', filterVoices);
    elements.languageFilter.addEventListener('change', filterVoices);
    elements.genderFilter.addEventListener('change', filterVoices);

    // File uploads (Index-TTS2)
    setupFileUpload();

    // File uploads (Coqui TTS)
    setupCoquiFileUpload();

    // Emotion control
    setupEmotionControl();

    // Text input
    setupTextInput();

    // Convert button
    elements.convertBtn.addEventListener('click', convertTextToSpeech);

    // Download button
    elements.downloadBtn.addEventListener('click', downloadAudio);
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();
    await checkEngines();
    await loadVoices();
    console.log('VoiceMaker initialized with dual-engine support');
    console.log('Edge-TTS: Ready');
    console.log('Index-TTS2:', state.indexTtsAvailable ? 'Ready' : 'Setup Required');
});
