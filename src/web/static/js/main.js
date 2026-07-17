class ChatbotUI {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.messagesContainer = document.getElementById('messages');
        this.modelSelect = document.getElementById('model');
        this.clearBtn = document.getElementById('clearBtn');
        this.exportBtn = document.getElementById('exportBtn');
        this.loading = document.getElementById('loading');
        this.charCount = document.getElementById('charCount');
        this.status = document.getElementById('status');
        
        this.initializeEventListeners();
    }
    
    initializeEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        this.clearBtn.addEventListener('click', () => this.clearHistory());
        this.exportBtn.addEventListener('click', () => this.exportConversation());
        this.messageInput.addEventListener('input', () => this.updateCharCount());
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) return;
        
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharCount();
        this.showLoading(true);
        
        try {
            const response = await this.makeRequest('/api/chat', {
                message: message,
                model: this.modelSelect.value
            });
            
            if (response.success) {
                this.addMessage(response.response, 'assistant');
            }
        } catch (error) {
            this.addMessage(`Erro: ${error.message}`, 'assistant');
        } finally {
            this.showLoading(false);
            this.messageInput.focus();
        }
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        messageDiv.appendChild(contentDiv);
        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    async clearHistory() {
        if (confirm('Limpar histórico?')) {
            await this.makeRequest('/api/clear-history', {});
            this.messagesContainer.innerHTML = '';
            this.addMessage('👋 Histórico limpo', 'assistant');
        }
    }
    
    async exportConversation() {
        await this.makeRequest('/api/export', {});
    }
    
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/2000`;
    }
    
    showLoading(show) {
        this.loading.classList.toggle('hidden', !show);
    }
    
    async makeRequest(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro desconhecido');
        }
        
        return await response.json();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chatbot = new ChatbotUI();
    console.log('🤖 GHS STUDIOS IA - Interface Carregada');
});