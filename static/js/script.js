document.addEventListener('DOMContentLoaded', function() {
    // Function to forcefully hide the loading indicator
    function hideLoadingIndicator() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.classList.add('hidden');
            loadingIndicator.style.display = 'none';
        }
    }
    
    // Function to show the loading indicator
    function showLoadingIndicator() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.classList.remove('hidden');
            loadingIndicator.style.display = 'flex';
        }
    }
    
    // Make sure indicator is hidden on page load
    hideLoadingIndicator();
    const form = document.getElementById('question-form');
    const chatMessages = document.getElementById('chat-messages');
    const questionInput = document.getElementById('question-input');
    const sendButton = document.getElementById('send-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const exampleQuestions = document.querySelectorAll('.example-question');

    // Set up example questions
    exampleQuestions.forEach(question => {
        question.addEventListener('click', function(e) {
            e.preventDefault();
            questionInput.value = this.textContent;
            questionInput.focus();
        });
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question) return;
        
        // Add user message to chat
        addMessage('user', question);
        
        // Clear input
        questionInput.value = '';
        
        // Disable input while waiting for response
        questionInput.disabled = true;
        sendButton.disabled = true;
        
        // Show loading indicator
        showLoadingIndicator();
        
        try {
            // Send question to backend
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });
            
            const data = await response.json();
            
            // Add AI response to chat
            if (data.error) {
                addMessage('error', data.answer);
                console.error('API Error:', data.answer);
            } else {
                addMessage('system', data.answer);
            }
        } catch (error) {
            addMessage('error', 'Sorry, there was an error processing your request. Please try again.');
            console.error('Error:', error);
        } finally {
            // Re-enable input
            questionInput.disabled = false;
            sendButton.disabled = false;
            questionInput.focus();
            
            // Hide loading indicator immediately
            hideLoadingIndicator();
            
            // Double-check that loading indicator is hidden after a slight delay
            setTimeout(hideLoadingIndicator, 100);
        }
    });

    // Function to add a message to the chat
    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        // Convert line breaks to <br> tags
        content = content.replace(/\n/g, '<br>');
        
        contentDiv.innerHTML = `<p>${content}</p>`;
        messageDiv.appendChild(contentDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
