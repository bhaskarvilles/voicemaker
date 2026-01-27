// ===== State Management =====
const state = {
    selectedVoice: null,
    allVoices: [],
    filteredVoices: [],
    resultAudioBlob: null
};

// ===== DOM Elements =====
const elements = {
    // Voice selection
    voiceGrid: document.getElementById('voiceGrid'),
    voiceSearch: document.getElementById('voiceSearch'),
    languageFilter: document.getElementById('languageFilter'),
    genderFilter: document.getElementById('genderFilter'),
    selectedVoiceDisplay: document.getElementById('selectedVoiceDisplay'),
    selectedVoiceName: document.getElementById('selectedVoiceName'),
    selectedVoiceLocale: document.getElementById('selectedVoiceLocale'),

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

// ===== Voice Loading and Filtering =====
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

// ===== Text Input Handler =====
function setupTextInput() {
    elements.textInput.addEventListener('input', (e) => {
        const length = e.target.value.length;
        elements.charCount.textContent = length;
    });
}

// ===== Conversion Handler =====
async function convertTextToSpeech() {
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
        showLoading('Generating speech...');

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

function downloadAudio() {
    if (!state.resultAudioBlob) {
        showNotification('No audio to download', 'error');
        return;
    }

    const url = URL.createObjectURL(state.resultAudioBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `voicemaker_${Date.now()}.mp3`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Audio downloaded!', 'success');
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Voice search and filters
    elements.voiceSearch.addEventListener('input', filterVoices);
    elements.languageFilter.addEventListener('change', filterVoices);
    elements.genderFilter.addEventListener('change', filterVoices);

    // Text input
    setupTextInput();

    // Convert button
    elements.convertBtn.addEventListener('click', convertTextToSpeech);

    // Download button
    elements.downloadBtn.addEventListener('click', downloadAudio);
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadVoices();
    console.log('VoiceMaker initialized with Edge-TTS');
});
