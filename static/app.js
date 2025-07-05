class ChatBot {
    constructor() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.typingIndicator = document.getElementById('typing-indicator');

        this.initializeEventListeners();
        this.addWelcomeMessage();
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }

    addWelcomeMessage() {
        const welcomeMessage = "Hello! I'm your virtual assistant. How can I help you today?";
        this.addMessage(welcomeMessage, 'bot');
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();

        if (!message) {
            return;
        }

        // Disable input while processing
        this.setInputState(false);

        // Add user message to chat
        this.addMessage(message, 'user');

        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send message to backend
            const response = await this.sendToBackend(message);

            // Hide typing indicator
            this.hideTypingIndicator();

            // Add bot response to chat
            if (response.success) {
                this.addMessage(response.response, 'bot');
            } else {
                this.addMessage(response.response || 'Sorry, something went wrong.', 'bot');
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting. Please try again.', 'bot');
        }

        // Re-enable input
        this.setInputState(true);
    }

    async sendToBackend(message) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = message;

        const timestamp = document.createElement('div');
        timestamp.className = 'timestamp';
        timestamp.textContent = this.getCurrentTime();

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timestamp);

        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;

        if (enabled) {
            this.messageInput.focus();
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Export for potential external use
window.ChatBot = ChatBot;
