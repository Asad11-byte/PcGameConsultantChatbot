
// ================================
// Auth0 Configuration
// ================================

let currentSessionId = null;
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
    const chatBox = document.getElementById("chatBox");
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

        loadChatHistory();
        userName.textContent = `👤 ${user.name}`;

        loginBtn.style.display = "none";
        logoutBtn.style.display = "block";
        // Switch from landing page to chat dashboard
        document.getElementById("landingScreen").classList.add("hidden");
        document.getElementById("chatScreen").classList.remove("hidden");

        // Show chat messages area
        document.getElementById("chatBox").classList.remove("hidden");

        const pendingPrompt = localStorage.getItem("pendingPrompt");

        if (pendingPrompt) {

            document.getElementById("userInput").value = pendingPrompt;

            localStorage.removeItem("pendingPrompt");

            sendMessage();

        }

    } else {

        userName.textContent = "";

        loginBtn.style.display = "block";
        logoutBtn.style.display = "none";
        // Show landing page
        document.getElementById("landingScreen").classList.remove("hidden");
        document.getElementById("chatScreen").classList.add("hidden");

    }

}
// ================================
// Login Button
// ================================

document.getElementById("loginBtn").addEventListener("click", async () => {

    if (!auth0Client) return;

    await auth0Client.loginWithRedirect();

});
document.getElementById("landingLoginBtn").addEventListener("click", async () => {

    if (!auth0Client) return;

    await auth0Client.loginWithRedirect();

});
// ================================
// Landing Page Signup Button
// ================================

document.getElementById("landingSignupBtn").addEventListener("click", async () => {

    if (!auth0Client) return;

    await auth0Client.loginWithRedirect({

        authorizationParams: {

            screen_hint: "signup"

        }

    });

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
// Send Chat Message 
// ================================

async function sendMessage() {

    const input = document.getElementById("userInput");
    const text = input.value.trim();

    if (!text) return;


    appendMessage(text, "user");
    input.value = "";

    const assistant = appendMessage("", "assistant");

    // User must be logged in
    if (!auth0Client || !(await auth0Client.isAuthenticated())) {
        assistant.textContent = "❌ Please log in first.";
        return;
    }

    // Get logged-in Auth0 user
    const user = await auth0Client.getUser();

    console.log("User:", user);

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: text,

                user: user,

                session_id: currentSessionId

            })

        });
        // ================================
        // Load Existing Chat
        // ================================

        
        if (window.innerWidth <= 768) {

            document
                .querySelector(".sidebar")
                .classList.remove("active");

        }
        const sessionId = response.headers.get(
            "X-Session-Id"
        );

        if (sessionId) {

            currentSessionId = sessionId;

            console.log(
                "Current Session:",
                currentSessionId
            );
            loadChatHistory();

        }

        if (!response.ok) {

            const error = await response.text();

            throw new Error(error);

        }

       const reader = response.body.getReader();

const decoder = new TextDecoder();

let fullResponse = "";

while (true) {

    const { done, value } = await reader.read();

    if (done) break;

    fullResponse += decoder.decode(value, { stream: true });

    assistant.innerHTML = marked.parse(fullResponse);

    document.getElementById("chatBox").scrollTop =
        document.getElementById("chatBox").scrollHeight;

}

} catch (err) {

    console.error(err);

    assistant.innerHTML = `
        <strong>❌ Error:</strong> ${err.message}
    `;

}
async function loadChatHistory() {

    if (!auth0Client) return;


    const user = await auth0Client.getUser();


    const response = await fetch(
        "/api/chat/history",
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: "history",

                user: user

            })

        }
    );


    const data = await response.json();


    const history =
        document.getElementById("chatHistory");


    history.innerHTML = "";


    data.chats.forEach(chat => {


        const div =
            document.createElement("div");


        div.className = "chat-item";


        div.textContent =
            chat.title;


        div.onclick = () => {

            openChat(chat.id);

        };


        history.appendChild(div);


    });

}
async function openChat(sessionId) {

            currentSessionId = sessionId;


            const response = await fetch(
                `/api/chat/${sessionId}`
            );


            const data = await response.json();


            const chatBox = document.getElementById("chatBox");


            chatBox.innerHTML = "";


            data.messages.forEach(msg => {

                appendMessage(
                    msg.content,
                    msg.role === "user"
                        ? "user"
                        : "assistant"
                );

            });

        }


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
// Append Message
// ================================

function appendMessage(text, sender) {

    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");

    div.className = `message ${sender}`;

    if (sender === "assistant") {

        div.innerHTML = marked.parse(text);

    } else {

        div.textContent = text;

    }

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

    return div;

}

async function loadChatHistory() {

    if (!auth0Client) return;


    const user = await auth0Client.getUser();


    const response = await fetch(
        "/api/chat/history",
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: "history",

                user: user

            })

        }
    );


    const data = await response.json();


    const history =
        document.getElementById("chatHistory");


    history.innerHTML = "";


    data.chats.forEach(chat => {

    const div = document.createElement("div");

    div.className = "chat-item";

    div.innerHTML = `
        <span class="chat-title">${chat.title}</span>

        <div class="chat-actions">

            <button class="chat-edit" title="Rename">
                ✏️
            </button>

            <button class="chat-delete" title="Delete">
                🗑️
            </button>

        </div>
    `;

    // Open chat
    div.querySelector(".chat-title").onclick = () => {

        openChat(chat.id);

    };

    // Rename
    div.querySelector(".chat-edit").onclick = (e) => {

        e.stopPropagation();

        renameChat(chat.id, chat.title);

    };

    // Delete
    div.querySelector(".chat-delete").onclick = (e) => {

        e.stopPropagation();

        deleteChat(chat.id);

    };

    history.appendChild(div);

});

}

// ================================
// Start Application
// ================================

window.addEventListener("load", () => {

    console.log("Application Started");

    console.log("Auth0 SDK:", typeof createAuth0Client);

    // Authorization parameters for Auth0 initialization
    initAuth({
        authorizationParams: {
            redirect_uri: window.location.origin,
            audience: "https://pc-game-consultant-api"
        }
    });

    document.querySelectorAll(".prompt-card").forEach(card => {

        card.addEventListener("click", async () => {

            const prompt = card.textContent.trim();

            if (await auth0Client.isAuthenticated()) {

                document.getElementById("userInput").value = prompt;

                sendMessage();

            } else {

                localStorage.setItem("pendingPrompt", prompt);

                await auth0Client.loginWithRedirect();

            }

        });

    });

document.getElementById("newChatBtn").addEventListener("click", () => {

    currentSessionId = null;

    document.getElementById("chatBox").innerHTML = "";

    document.getElementById("userInput").value = "";

    document.getElementById("userInput").focus();

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {

        document
            .querySelector(".sidebar")
            .classList.remove("active");

    }

});

    // ======================================
// Mobile Sidebar
// ======================================

const menuBtn = document.getElementById("menuBtn");
const sidebar = document.querySelector(".sidebar");

// Create overlay
const overlay = document.createElement("div");
overlay.className = "sidebar-overlay";
document.body.appendChild(overlay);

// Open / Close sidebar
menuBtn.addEventListener("click", () => {

    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");

});

// Close when clicking overlay
overlay.addEventListener("click", closeSidebar);

// Close with ESC
document.addEventListener("keydown", (e) => {

    if (e.key === "Escape") {
        closeSidebar();
    }

});

function closeSidebar() {

    sidebar.classList.remove("active");
    overlay.classList.remove("active");

}

// Automatically close after selecting a chat (mobile only)
document.addEventListener("click", (e) => {

    if (window.innerWidth <= 768 && e.target.closest(".chat-item")) {
        closeSidebar();
    }

});
// ======================================
// Rename Chat
// ======================================

async function renameChat(chatId, currentTitle) {

    const newTitle = prompt(
        "Rename conversation:",
        currentTitle
    );

    if (
        !newTitle ||
        newTitle.trim() === "" ||
        newTitle === currentTitle
    ) {
        return;
    }

    try {

        const response = await fetch(
            `/api/chat/${chatId}/rename`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    title: newTitle.trim()
                })
            }
        );

        if (!response.ok) {

            throw new Error("Unable to rename chat.");

        }

        loadChatHistory();

    } catch (err) {

        console.error(err);

        alert(err.message);

    }

}


