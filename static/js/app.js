document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Initialize Lucide icons
    lucide.createIcons();

    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';

        // Enable/disable send button based on input
        const hasContent = messageInput.value.trim().length > 0;
        sendButton.disabled = !hasContent;
        sendButton.className = `absolute right-2 bottom-2.5 p-1.5 rounded-lg ${
            hasContent ? 'bg-green-500 text-white hover:bg-green-600' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
        }`;
    });

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        messageInput.value = '';
        messageInput.style.height = 'auto';
        sendButton.disabled = true;
        sendButton.className = 'absolute right-2 bottom-2.5 p-1.5 rounded-lg bg-gray-200 text-gray-400 cursor-not-allowed';

        // Show loading state
        const loadingDiv = addLoadingState();

        try {
            // Send message to server
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();

            // Remove loading state
            loadingDiv.remove();

            // Add assistant response
            addMessage(data.response, 'assistant');
        } catch (error) {
            console.error('Error:', error);
            loadingDiv.remove();
            addMessage('Sorry, there was an error processing your request.', 'assistant');
        }
    });

    // Handle Enter key
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!messageInput.value.trim()) return;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    function addMessage(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `px-4 py-8 ${role === 'assistant' ? 'bg-white' : 'bg-gray-50'}`;

        const innerDiv = document.createElement('div');
        innerDiv.className = 'max-w-3xl mx-auto flex gap-4';

        const iconDiv = document.createElement('div');
        iconDiv.className = 'mt-1';

        const avatarDiv = document.createElement('div');
        avatarDiv.className = `w-8 h-8 rounded-full ${role === 'assistant' ? 'bg-green-500' : 'bg-gray-500'} flex items-center justify-center`;

        const icon = document.createElement('i');
        icon.setAttribute('data-lucide', role === 'assistant' ? 'bot' : 'user');
        icon.className = 'w-5 h-5 text-white';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'prose prose-sm max-w-none';

        content.split('\n').forEach(line => {
            const p = document.createElement('p');
            p.className = 'mb-4';
            p.textContent = line;
            contentDiv.appendChild(p);
        });

        avatarDiv.appendChild(icon);
        iconDiv.appendChild(avatarDiv);
        innerDiv.appendChild(iconDiv);
        innerDiv.appendChild(contentDiv);
        messageDiv.appendChild(innerDiv);
        chatMessages.appendChild(messageDiv);

        // Initialize the new icon
        lucide.createIcons();

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addLoadingState() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'px-4 py-8 bg-white';
        loadingDiv.innerHTML = `
            <div class="max-w-3xl mx-auto flex gap-4">
                <div class="mt-1">
                    <div class="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                        <i data-lucide="bot" class="w-5 h-5 text-white"></i>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <div class="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                    <div class="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style="animation-delay: 200ms"></div>
                    <div class="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style="animation-delay: 400ms"></div>
                </div>
            </div>
        `;
        chatMessages.appendChild(loadingDiv);
        lucide.createIcons();
        return loadingDiv;
    }
});