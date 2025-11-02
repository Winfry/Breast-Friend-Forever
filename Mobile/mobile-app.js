// Breast Friend Forever Mobile App
class BFFMobileApp {
    constructor() {
        this.currentTab = 'chat';
        this.apiBaseUrl = '/api/mobile';
        this.isOnline = navigator.onLine;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupNetworkMonitoring();
        this.registerServiceWorker();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-btn, .nav-item').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const tab = btn.dataset.tab;
                this.switchTab(tab);
            });
        });

        // Menu toggle
        document.getElementById('menuButton').addEventListener('click', () => {
            document.getElementById('navMenu').classList.add('active');
        });

        document.getElementById('closeMenu').addEventListener('click', () => {
            document.getElementById('navMenu').classList.remove('active');
        });

        // Chat functionality
        document.getElementById('sendButton').addEventListener('click', () => this.sendMessage());
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Quick suggestions
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const message = btn.dataset.message;
                document.getElementById('chatInput').value = message;
                this.sendMessage();
            });
        });

        // Hospital search
        document.getElementById('searchButton').addEventListener('click', () => this.searchHospitals());

        // Health tips
        document.getElementById('dailyTipBtn').addEventListener('click', () => this.getDailyTip());
        document.getElementById('randomTipBtn').addEventListener('click', () => this.getRandomTips());

        // Self-exam
        document.getElementById('setReminderBtn').addEventListener('click', () => this.setExamReminder());

        // Emergency
        document.getElementById('callEmergency').addEventListener('click', () => this.callEmergency());
        document.getElementById('findNearest').addEventListener('click', () => this.findNearestHospital());
    }

    switchTab(tabName) {
        // Update active tab
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.nav-btn, .nav-item').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        document.querySelectorAll(`[data-tab="${tabName}"]`).forEach(btn => {
            btn.classList.add('active');
        });

        // Close mobile menu if open
        document.getElementById('navMenu').classList.remove('active');

        this.currentTab = tabName;

        // Load tab-specific data
        this.loadTabData(tabName);
    }

    async loadTabData(tabName) {
        switch(tabName) {
            case 'hospitals':
                await this.loadHospitalFilters();
                break;
            case 'self-exam':
                await this.loadExamGuide();
                break;
            case 'emergency':
                await this.loadEmergencyContacts();
                break;
        }
    }

    async loadInitialData() {
        // Load any initial data needed
        await this.loadHospitalFilters();
    }

    // Chat functionality
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await this.apiCall('/chat', 'POST', {
                message: message
            });

            this.removeTypingIndicator();
            this.addMessage(response.response, 'bot', response.suggestions);
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage(
                "I'm having trouble connecting right now. Please check your internet connection and try again.", 
                'bot',
                ["Try again", "Check connection", "Emergency contacts"]
            );
            console.error('Chat error:', error);
        }
    }

    addMessage(content, sender, suggestions = null) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-content">${content}</div>
            <div class="message-time">${timestamp}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Update quick suggestions if provided
        if (suggestions && sender === 'bot') {
            this.updateQuickSuggestions(suggestions);
        }
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    updateQuickSuggestions(suggestions) {
        const container = document.getElementById('quickSuggestions');
        container.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const button = document.createElement('button');
            button.className = 'suggestion-btn';
            button.textContent = suggestion;
            button.dataset.message = suggestion;
            button.addEventListener('click', () => {
                document.getElementById('chatInput').value = suggestion;
                this.sendMessage();
            });
            container.appendChild(button);
        });
    }

    // Hospital search functionality
    async loadHospitalFilters() {
        try {
            const [countiesResponse, servicesResponse] = await Promise.all([
                this.apiCall('/hospitals/counties'),
                this.apiCall('/hospitals/services')
            ]);

            this.populateSelect('countyFilter', countiesResponse.counties);
            this.populateSelect('serviceFilter', servicesResponse.services);
        } catch (error) {
            console.error('Error loading hospital filters:', error);
        }
    }

    populateSelect(selectId, options) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">All</option>';
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
    }

    async searchHospitals() {
        const county = document.getElementById('countyFilter').value;
        const service = document.getElementById('serviceFilter').value;

        const resultsContainer = document.getElementById('hospitalResults');
        resultsContainer.innerHTML = '<div class="loading">Searching for hospitals...</div>';

        try {
            const response = await this.apiCall('/hospitals/search', 'POST', {
                county: county || null,
                service: service || null
            });

            this.displayHospitalResults(response.facilities);
        } catch (error) {
            resultsContainer.innerHTML = `
                <div class="error-message">
                    ${error.message || 'Failed to search hospitals. Please try again.'}
                </div>
            `;
        }
    }

    displayHospitalResults(hospitals) {
        const container = document.getElementById('hospitalResults');
        
        if (hospitals.length === 0) {
            container.innerHTML = '<div class="loading">No hospitals found matching your criteria.</div>';
            return;
        }

        container.innerHTML = hospitals.map(hospital => `
            <div class="hospital-card">
                <div class="hospital-name">${hospital.name}</div>
                <div class="hospital-info">
                    <div>📍 ${hospital.county} County</div>
                    <div>📞 ${hospital.phone}</div>
                    <div>🕒 ${hospital.hours}</div>
                    ${hospital.emergency ? '<div>🚨 Emergency Services Available</div>' : ''}
                </div>
                <div class="hospital-services">
                    ${hospital.services.map(service => 
                        `<span class="service-tag">${service}</span>`
                    ).join('')}
                </div>
                <div class="hospital-actions">
                    <button class="action-btn" onclick="app.callHospital('${hospital.phone}')">📞 Call</button>
                    <button class="action-btn" onclick="app.getDirections('${hospital.name}')">📍 Directions</button>
                </div>
            </div>
        `).join('');
    }

    // Health tips functionality
    async getDailyTip() {
        try {
            const response = await this.apiCall('/health-tips/daily');
            this.displayTip(response.tip, true);
        } catch (error) {
            this.displayTip("Stay hydrated and maintain a balanced diet for overall health.", false);
        }
    }

    async getRandomTips() {
        try {
            const response = await this.apiCall('/health-tips?count=1');
            this.displayTip(response.tips[0], false);
        } catch (error) {
            this.displayTip("Regular exercise helps maintain healthy body weight and reduces cancer risk.", false);
        }
    }

    displayTip(tip, isDaily = false) {
        const container = document.getElementById('tipsDisplay');
        container.innerHTML = `
            <div class="tip-card">
                <div class="tip-icon">${isDaily ? '⭐' : '💡'}</div>
                <div class="tip-content">
                    <p>${tip}</p>
                    ${isDaily ? '<small>✨ Your daily tip</small>' : ''}
                </div>
            </div>
        `;
    }

    // Self-exam functionality
    async loadExamGuide() {
        try {
            const response = await this.apiCall('/self-exam/guide');
            this.displayExamSteps(response.steps);
        } catch (error) {
            console.error('Error loading exam guide:', error);
        }
    }

    displayExamSteps(steps) {
        const container = document.getElementById('examSteps');
        container.innerHTML = steps.map(step => `
            <div class="step-card">
                <div class="step-number">${step.step}</div>
                <div class="step-title">${step.title}</div>
                <div class="step-description">${step.description}</div>
                <div class="step-duration">⏱️ ${step.duration}</div>
            </div>
        `).join('');
    }

    async setExamReminder() {
        if ('Notification' in window && Notification.permission === 'granted') {
            // Schedule notification logic here
            this.showNotification('Reminder set!', 'Monthly breast self-exam reminder has been scheduled.');
        } else if (Notification.permission !== 'denied') {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.showNotification('Reminder set!', 'Monthly self-exam reminders activated.');
            }
        }
    }

    // Emergency functionality
    async loadEmergencyContacts() {
        try {
            const response = await this.apiCall('/emergency/contacts');
            this.displayEmergencyContacts(response.emergency_contacts);
        } catch (error) {
            console.error('Error loading emergency contacts:', error);
        }
    }

    displayEmergencyContacts(contacts) {
        const container = document.getElementById('contactsList');
        container.innerHTML = contacts.map(contact => `
            <div class="contact-card">
                <div class="contact-info">
                    <div class="contact-service">${contact.service}</div>
                    <div class="contact-phone">${contact.phone}</div>
                    <div class="contact-hours">${contact.hours}</div>
                </div>
                <button class="call-btn" onclick="app.callNumber('${contact.phone}')">📞</button>
            </div>
        `).join('');
    }

    callEmergency() {
        this.callNumber('999');
    }

    async findNearestHospital() {
        // This would use geolocation in a real app
        this.switchTab('hospitals');
        // Auto-search for hospitals in current location
        setTimeout(() => {
            document.getElementById('countyFilter').value = 'Nairobi'; // Example
            this.searchHospitals();
        }, 500);
    }

    // Utility methods
    callNumber(phoneNumber) {
        if (confirm(`Call ${phoneNumber}?`)) {
            window.location.href = `tel:${phoneNumber}`;
        }
    }

    callHospital(phoneNumber) {
        this.callNumber(phoneNumber);
    }

    getDirections(hospitalName) {
        // In a real app, this would open maps with the hospital location
        const mapsUrl = `https://maps.google.com/?q=${encodeURIComponent(hospitalName + ' Kenya')}`;
        window.open(mapsUrl, '_blank');
    }

    showNotification(title, body) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, { body, icon: '/static/icons/icon-192x192.png' });
        }
    }

    async apiCall(endpoint, method = 'GET', data = null) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }

        return await response.json();
    }

    setupNetworkMonitoring() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.showOnlineStatus();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.showOfflineStatus();
        });
    }

    showOnlineStatus() {
        this.showTempMessage('Connection restored', 'success');
    }

    showOfflineStatus() {
        this.showTempMessage('You are currently offline', 'error');
    }

    showTempMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `temp-message ${type}-message`;
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            padding: 10px 20px;
            border-radius: 20px;
            background: ${type === 'error' ? '#DC3545' : type === 'success' ? '#28A745' : '#FF69B4'};
            color: white;
            z-index: 1000;
            animation: slideDown 0.3s ease;
        `;

        document.body.appendChild(messageDiv);

        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.ready.then(() => {
                console.log('Service Worker is ready');
            });
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BFFMobileApp();
});

// Add some CSS for temporary messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    
    .typing-dots {
        display: inline-flex;
        gap: 4px;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #999;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
`;
document.head.appendChild(style);