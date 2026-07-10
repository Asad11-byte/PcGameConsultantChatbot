// ================================
// Auth0 Configuration
// ================================

let auth0Client = null;

async function initAuth() {
    try {
        console.log("Initializing Auth0...");

        auth0Client = await auth0.createAuth0Client({
            domain: "dev-dcrde617po8vb5xc.us.auth0.com",
            clientId: "P79g2Q0xoLPq7Dsjq4WdsxAuhAwop8hX",
            authorizationParams: {
                redirect_uri: window.location.origin
            }
        });

        console.log("✅ Auth0 initialized");

        // Handle Auth0 redirect
        if (
            window.location.search.includes("code=") &&
            window.location.search.includes("state=")
        ) {
            await auth0Client.handleRedirectCallback();

            window.history.replaceState(
                {},
                document.title,
                window.location.pathname
            );
        }

        updateUI();

    } catch (err) {
        console.error("❌ Auth0 Initialization Error:", err);
    }
}
const scrollToBottom = () => {
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
};

// Example Trigger Usage: Call this right after adding any message element to the DOM
// appendUserMessage();
// scrollToBottom();
async function updateUI() {

    if (!auth0Client) return;

    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const userName = document.getElementById("userName");

    const authenticated = await auth0Client.isAuthenticated();

    if (authenticated) {

        const user = await auth0Client.getUser();

        userName.textContent = `👤 ${user.name}`;

        loginBtn.style.display = "none";
        logoutBtn.style.display = "block";

        console.log("Logged in:", user);

    } else {

        userName.textContent = "";

        loginBtn.style.display = "block";
        logoutBtn.style.display = "none";

        console.log("User not logged in");

    }
}

// ================================
// Login Button
// ================================

document.getElementById("loginBtn").addEventListener("click", async () => {

    if (!auth0Client) return;

    await auth0Client.loginWithRedirect();

});

// ================================
// Logout Button
// ================================

document.getElementById("logoutBtn").addEventListener("click", () => {

    if (!auth0Client) return;

    auth0Client.logout({

        logoutParams: {

            returnTo: window.location.origin

        }

    });

});

// ================================
// Slider Updates
// ================================

document.getElementById("temperature").addEventListener("input", e => {

    document.getElementById("tempValue").textContent = e.target.value;

});

document.getElementById("topP").addEventListener("input", e => {

    document.getElementById("topPValue").textContent = e.target.value;

});

document.getElementById("maxTokens").addEventListener("input", e => {

    document.getElementById("tokensValue").textContent = e.target.value;

});

// ================================
// Chat Events
// ================================

document.getElementById("sendBtn").addEventListener("click", sendMessage);

document.getElementById("userInput").addEventListener("keypress", e => {

    if (e.key === "Enter") {

        sendMessage();

    }

});

// ================================
// Send Chat Message
// ================================

async function sendMessage() {

    const input = document.getElementById("userInput");

    const text = input.value.trim();

    if (!text) return;

    appendMessage(text, "user");

    input.value = "";

    const assistant = appendMessage("", "assistant");

    try {

        const response = await fetch("http://127.0.0.1:8000/api/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: text,

                system_prompt: document.getElementById("systemPrompt").value,

                temperature: parseFloat(document.getElementById("temperature").value),

                top_p: parseFloat(document.getElementById("topP").value),

                max_tokens: parseInt(document.getElementById("maxTokens").value)

            })

        });

        if (!response.ok) {

            throw new Error(`HTTP ${response.status}`);

        }

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            assistant.textContent += decoder.decode(value);

            document.getElementById("chatBox").scrollTop =
                document.getElementById("chatBox").scrollHeight;
        }

    } catch (err) {

        assistant.textContent = "❌ " + err.message;

        console.error(err);

    }

}

// ================================
// Append Message
// ================================

function appendMessage(text, sender) {

    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");

    div.className = `message ${sender}`;

    div.textContent = text;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

    return div;

}

// ================================
// Start Application
// ================================

window.addEventListener("load", () => {

    console.log("Application Started");

    console.log("Auth0 SDK:", typeof createAuth0Client);

    initAuth();

});