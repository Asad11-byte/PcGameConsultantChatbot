document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

async function sendMessage() {
    const inputField = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');
    const text = inputField.value.trim();

    if (!text) return;

    // 1. Append User Text Node to UI Container
    appendMessage(text, 'user');
    inputField.value = '';

    // 2. Inject initial placeholder element block for the stream
    const assistantMessageDiv = appendMessage('', 'assistant');

    try {
        // 3. Dispatch the payload matching our Pydantic schema structure
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) throw new Error("Server communication faulted.");

        // 4. Hook up a stream reader interface
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunkText = decoder.decode(value, { stream: true });
            // Add text tokens smoothly onto UI screen element container
            assistantMessageDiv.textContent += chunkText;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (err) {
        assistantMessageDiv.textContent = `Error: ${err.message}`;
        assistantMessageDiv.style.color = '#ff4a4a';
    }
}

function appendMessage(text, sender) {
    const chatBox = document.getElementById('chatBox');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}