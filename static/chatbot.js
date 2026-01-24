document.addEventListener('DOMContentLoaded', function() {
    const chatlog = document.getElementById('chatlog');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get user input
        const userMessage = userInput.value;

        // Clear the input field
        userInput.value = '';

        // Add the user message to the chat log
        chatlog.innerHTML += '<p class="user-message">' + userMessage + '</p>';

        // Send the user message to the server and get the response
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            body: 'user_input=' + encodeURIComponent(userMessage)
        })
        .then(response => response.json())
        .then(data => {
            // Add the bot response to the chat log
            chatlog.innerHTML += '<p class="bot-message">' + data.bot_response + '</p>';
            // Scroll to the bottom of the chat log
            chatlog.scrollTop = chatlog.scrollHeight;
        });
    });
});