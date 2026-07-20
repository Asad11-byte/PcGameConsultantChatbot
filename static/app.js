// ============================================================================
// 1. GLOBAL STATE & AUTH CONFIGURATION
// ============================================================================

let currentSessionId = null;
let auth0Client = null;

/**
 * Retrieves the current Auth0 Access Token for API requests.
 */
async function getAccessToken() {
    if (!auth0Client) return null;
    try {
        return await auth0Client.getTokenSilently();
    } catch (err) {
        console.error("Failed to get access token:", err);
        return null;
    }
}

// ============================================================================
// 2. UI HELPERS & MOBILE SIDEBAR NAVIGATION
// ============================================================================

const scrollToBottom = () => {
    const chatBox = document.getElementById("chatBox");
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
};

function appendMessage(text, sender) {
    const chatBox = document.getElementById("chatBox");
    const div = document.createElement("div");

    div.className = `message ${sender}`;

    if (sender === "assistant") {
        div.innerHTML = typeof marked !== "undefined" ? marked.parse(text) : text;
    } else {
        div.textContent = text;
    }

    chatBox.appendChild(div);
    scrollToBottom();

    return div;
}

function closeSidebar() {
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");

    if (sidebar) sidebar.classList.remove("active");
    if (overlay) overlay.classList.remove("active");
}

function setupMobileSidebar() {
    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.querySelector(".sidebar");

    if (!menuBtn || !sidebar) return;

    // Create overlay once if missing
    let overlay = document.querySelector(".sidebar-overlay");
    if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "sidebar-overlay";
        document.body.appendChild(overlay);
    }

    // Toggle sidebar
    menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("active");
        overlay.classList.toggle("active");
    });

    // Close on overlay click
    overlay.addEventListener("click", closeSidebar);

    // Close on Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeSidebar();
    });

    // Auto-close on mobile when clicking a chat item
    document.addEventListener("click", (e) => {
        if (window.innerWidth <= 768 && e.target.closest(".chat-item")) {
            closeSidebar();
        }
    });
}

// ============================================================================
// 3. AUTH0 INITIALIZATION & UI STATE MANAGEMENT
// ============================================================================

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

        // Handle Auth0 redirect after login
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

        await updateUI();

    } catch (err) {
        console.error("❌ Auth0 Initialization Error:", err);
    }
}

async function updateUI() {
    if (!auth0Client) return;

    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const userName = document.getElementById("userName");

    const authenticated = await auth0Client.isAuthenticated();

    if (authenticated) {
        const user = await auth0Client.getUser();

        loadChatHistory();
        if (userName) userName.textContent = `👤 ${user.name}`;

        if (loginBtn) loginBtn.style.display = "none";
        if (logoutBtn) logoutBtn.style.display = "block";

        // View switching
        document.getElementById("landingScreen")?.classList.add("hidden");
        document.getElementById("chatScreen")?.classList.remove("hidden");
        document.getElementById("chatBox")?.classList.remove("hidden");

        // Check for pending prompts stored prior to authentication
        const pendingPrompt = localStorage.getItem("pendingPrompt");
        if (pendingPrompt) {
            const userInput = document.getElementById("userInput");
            if (userInput) userInput.value = pendingPrompt;
            localStorage.removeItem("pendingPrompt");
            sendMessage();
        }

    } else {
        if (userName) userName.textContent = "";
        if (loginBtn) loginBtn.style.display = "block";
        if (logoutBtn) logoutBtn.style.display = "none";

        document.getElementById("landingScreen")?.classList.remove("hidden");
        document.getElementById("chatScreen")?.classList.add("hidden");
    }
}

// ============================================================================
// 4. CHAT API LOGIC & OPERATIONS
// ============================================================================

async function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input ? input.value.trim() : "";

    if (!text) return;

    appendMessage(text, "user");
    if (input) input.value = "";

    const assistant = appendMessage("", "assistant");

    if (!auth0Client || !(await auth0Client.isAuthenticated())) {
        assistant.textContent = "❌ Please log in first.";
        return;
    }

    const user = await auth0Client.getUser();

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

        // Close mobile drawer on submission
        if (window.innerWidth <= 768) {
            closeSidebar();
        }

        const sessionId = response.headers.get("X-Session-Id");
        if (sessionId) {
            currentSessionId = sessionId;
            loadChatHistory();
        }

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }

        // Stream reader setup
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            fullResponse += decoder.decode(value, { stream: true });
            assistant.innerHTML = typeof marked !== "undefined" ? marked.parse(fullResponse) : fullResponse;
            scrollToBottom();
        }

    } catch (err) {
        console.error("Send Message Error:", err);
        assistant.innerHTML = `<strong>❌ Error:</strong> ${err.message}`;
    }
}

async function openChat(sessionId) {
    currentSessionId = sessionId;

    try {
        const response = await fetch(`/api/chat/${sessionId}`);
        const data = await response.json();

        const chatBox = document.getElementById("chatBox");
        if (chatBox) chatBox.innerHTML = "";

        if (data.messages && Array.isArray(data.messages)) {
            data.messages.forEach(msg => {
                appendMessage(
                    msg.content,
                    msg.role === "user" ? "user" : "assistant"
                );
            });
        }
    } catch (err) {
        console.error("Open Chat Error:", err);
    }
}

async function loadChatHistory() {
    if (!auth0Client) return;

    const user = await auth0Client.getUser();

    try {
        const response = await fetch("/api/chat/history", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: "history",
                user: user
            })
        });

        const data = await response.json();
        const historyContainer = document.getElementById("chatHistory");

        if (!historyContainer) return;
        historyContainer.innerHTML = "";

        if (!data.chats || !Array.isArray(data.chats)) return;

        data.chats.forEach(chat => {
            const div = document.createElement("div");
            div.className = "chat-item";

            div.innerHTML = `
                <span class="chat-title">${chat.title}</span>
                <div class="chat-actions">
                    <button class="chat-edit" title="Rename">✏️</button>
                    <button class="chat-delete" title="Delete">🗑️</button>
                </div>
            `;

            // Item action bindings
            div.querySelector(".chat-title").onclick = () => openChat(chat.id);

            div.querySelector(".chat-edit").onclick = (e) => {
                e.stopPropagation();
                renameChat(chat.id, chat.title);
            };

            div.querySelector(".chat-delete").onclick = (e) => {
                e.stopPropagation();
                deleteChat(chat.id);
            };

            historyContainer.appendChild(div);
        });

    } catch (err) {
        console.error("Load Chat History Error:", err);
    }
}

async function deleteChat(chatId) {
    if (!confirm("Are you sure you want to delete this chat?")) {
        return;
    }

    const token = await getAccessToken();

    try {
        const response = await fetch(`/api/chat/${chatId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Unable to delete chat.");
        }

        loadChatHistory();

        // Clear chat screen if currently viewing deleted chat
        if (currentSessionId === chatId) {
            currentSessionId = null;
            const chatBox = document.getElementById("chatBox");
            if (chatBox) chatBox.innerHTML = "";
        }

    } catch (err) {
        console.error("Delete Chat Error:", err);
        alert(err.message);
    }
}

async function renameChat(chatId, currentTitle) {
    const newTitle = prompt("Rename conversation:", currentTitle);

    if (!newTitle || newTitle.trim() === "" || newTitle === currentTitle) {
        return;
    }

    const token = await getAccessToken();

    try {
        const response = await fetch(`/api/chat/${chatId}/rename`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                title: newTitle.trim()
            })
        });

        if (!response.ok) {
            throw new Error("Unable to rename chat.");
        }

        loadChatHistory();

    } catch (err) {
        console.error("Rename Chat Error:", err);
        alert(err.message);
    }
}

// ============================================================================
// 5. EVENT LISTENERS & APPLICATION INITIALIZATION
// ============================================================================

window.addEventListener("DOMContentLoaded", () => {
    console.log("Application Loaded");

    // Initialize Auth & UI
    initAuth();
    setupMobileSidebar();

    // Authentication buttons
    document.getElementById("loginBtn")?.addEventListener("click", async () => {
        if (auth0Client) await auth0Client.loginWithRedirect();
    });

    document.getElementById("landingLoginBtn")?.addEventListener("click", async () => {
        if (auth0Client) await auth0Client.loginWithRedirect();
    });

    document.getElementById("landingSignupBtn")?.addEventListener("click", async () => {
        if (auth0Client) {
            await auth0Client.loginWithRedirect({
                authorizationParams: { screen_hint: "signup" }
            });
        }
    });

    document.getElementById("logoutBtn")?.addEventListener("click", () => {
        if (auth0Client) {
            auth0Client.logout({
                logoutParams: { returnTo: window.location.origin }
            });
        }
    });

    // Chat form submissions
    document.getElementById("sendBtn")?.addEventListener("click", sendMessage);

    document.getElementById("userInput")?.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    // New Chat Action
    document.getElementById("newChatBtn")?.addEventListener("click", () => {
        currentSessionId = null;
        const chatBox = document.getElementById("chatBox");
        const userInput = document.getElementById("userInput");

        if (chatBox) chatBox.innerHTML = "";
        if (userInput) {
            userInput.value = "";
            userInput.focus();
        }

        closeSidebar();
    });

    // Prompt Card Click Handlers
    document.querySelectorAll(".prompt-card").forEach(card => {
        card.addEventListener("click", async () => {
            const promptText = card.textContent.trim();

            if (auth0Client && await auth0Client.isAuthenticated()) {
                const userInput = document.getElementById("userInput");
                if (userInput) userInput.value = promptText;
                sendMessage();
            } else if (auth0Client) {
                localStorage.setItem("pendingPrompt", promptText);
                await auth0Client.loginWithRedirect();
            }
        });
    });
});