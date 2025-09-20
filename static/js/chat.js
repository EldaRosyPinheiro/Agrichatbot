// Global variables
let isLoading = false;
let chatHistory = [];

// DOM Elements
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');
const charCount = document.getElementById('charCount');

// Initialize chat functionality
function setupEventListeners() {
    // Send message on Enter key
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Character count update
    messageInput.addEventListener('input', updateCharCount);

    // Auto-resize input (optional enhancement)
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // Focus on input when page loads
    messageInput.focus();
}

// Update character count
function updateCharCount() {
    const count = messageInput.value.length;
    charCount.textContent = `${count}/500`;
    
    if (count > 450) {
        charCount.style.color = '#f44336';
    } else if (count > 400) {
        charCount.style.color = '#ff9800';
    } else {
        charCount.style.color = '#999';
    }
}

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isLoading) {
        return;
    }

    // Validate message length
    if (message.length > 500) {
        showErrorMessage('Message is too long. Please keep it under 500 characters.');
        return;
    }

    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    messageInput.value = '';
    updateCharCount();
    
    // Show typing indicator
    showTypingIndicator();
    
    // Disable input while processing
    setInputState(false);
    
    try {
        // Send to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        if (data.status === 'success') {
            // Add bot response to chat
            addBotMessage(data.response);
        } else {
            showErrorMessage(data.error || 'Sorry, I encountered an error. Please try again.');
        }
        
    } catch (error) {
        hideTypingIndicator();
        showErrorMessage('Sorry, I\'m having trouble connecting. Please check your internet connection and try again.');
        console.error('Chat error:', error);
    } finally {
        // Re-enable input
        setInputState(true);
        messageInput.focus();
    }
}

// Add user message to chat
function addUserMessage(message) {
    const messageElement = createMessageElement(message, 'user');
    chatMessages.appendChild(messageElement);
    scrollToBottom();
    
    // Store in chat history
    chatHistory.push({
        type: 'user',
        message: message,
        timestamp: new Date().toISOString()
    });
}

// Add bot message to chat
function addBotMessage(message) {
    const messageElement = createMessageElement(message, 'bot');
    chatMessages.appendChild(messageElement);
    scrollToBottom();
    
    // Store in chat history
    chatHistory.push({
        type: 'bot',
        message: message,
        timestamp: new Date().toISOString()
    });
}

// Create message element
function createMessageElement(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = type === 'bot' ? '<i class="fas fa-seedling"></i>' : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const text = document.createElement('div');
    text.className = 'message-text';
    text.innerHTML = formatMessage(message);
    
    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = getCurrentTime();
    
    content.appendChild(text);
    content.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    return messageDiv;
}

// Format message with basic markdown and emojis
function formatMessage(message) {
    // Convert line breaks
    message = message.replace(/\n/g, '<br>');
    
    // Convert **bold** to <strong>
    message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    message = message.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert bullet points
    message = message.replace(/^• /gm, '&nbsp;&nbsp;• ');
    
    return message;
}

// Show typing indicator
function showTypingIndicator() {
    isLoading = true;
    typingIndicator.style.display = 'block';
    chatMessages.appendChild(typingIndicator);
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    isLoading = false;
    typingIndicator.style.display = 'none';
    if (typingIndicator.parentNode) {
        typingIndicator.parentNode.removeChild(typingIndicator);
    }
}

// Set input state (enabled/disabled)
function setInputState(enabled) {
    messageInput.disabled = !enabled;
    sendButton.disabled = !enabled;
    
    if (enabled) {
        messageInput.placeholder = 'Ask about crops, pests, soil, or farming techniques...';
        sendButton.style.opacity = '1';
    } else {
        messageInput.placeholder = 'Please wait...';
        sendButton.style.opacity = '0.5';
    }
}

// Show error message
function showErrorMessage(error) {
    const errorDiv = createMessageElement(`⚠️ ${error}`, 'bot');
    errorDiv.querySelector('.message-text').classList.add('error-message');
    chatMessages.appendChild(errorDiv);
    scrollToBottom();
}

// Send quick message from suggestion chips
function sendQuickMessage(message) {
    messageInput.value = message;
    sendMessage();
}

// Scroll to bottom of chat
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Get current time formatted
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
}

// Update time display
function updateTime() {
    const timeElement = document.getElementById('bot-time');
    if (timeElement) {
        timeElement.textContent = getCurrentTime();
    }
}

// Toggle chat (for minimize functionality)
function toggleChat() {
    const chatContainer = document.querySelector('.chat-container');
    const isMinimized = chatContainer.classList.contains('minimized');
    
    if (isMinimized) {
        chatContainer.classList.remove('minimized');
        chatContainer.style.height = '90vh';
    } else {
        chatContainer.classList.add('minimized');
        chatContainer.style.height = '60px';
    }
}

// Export chat history (optional feature)
function exportChatHistory() {
    const dataStr = JSON.stringify(chatHistory, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `agriculture-chat-${new Date().toISOString().slice(0,10)}.json`;
    link.click();
}

// Clear chat history
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        chatHistory = [];
        chatMessages.innerHTML = '';
        
        // Add welcome message back
        const welcomeMessage = `Hello! I'm your Agriculture Assistant. I can help you with:

🌱 **Crop cultivation** - Growing tips, varieties, seasons
🐛 **Pest management** - Identification and treatment
🌾 **Soil care** - Testing, fertilization, composting
🌧️ **Weather planning** - Seasonal guidelines
🌰 **Seeds & planting** - Selection and timing
📦 **Harvesting** - Techniques and storage

What would you like to know about farming today?`;
        
        addBotMessage(welcomeMessage);
    }
}

// Handle connection errors
window.addEventListener('online', function() {
    console.log('Connection restored');
    // Optionally show a message that connection is restored
});

window.addEventListener('offline', function() {
    console.log('Connection lost');
    showErrorMessage('Connection lost. Please check your internet connection.');
});

// Prevent form submission on page refresh
window.addEventListener('beforeunload', function(e) {
    if (messageInput.value.trim() && messageInput.value.trim().length > 10) {
        e.preventDefault();
        e.returnValue = 'You have unsent message. Are you sure you want to leave?';
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateTime();
    
    // Update time every minute
    setInterval(updateTime, 60000);
    
    console.log('Agriculture Chatbot initialized successfully');
});
