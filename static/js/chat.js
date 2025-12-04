const messagesContainer = document.getElementById("messagesContainer");
const emptyState = document.getElementById("emptyState");
const inputField = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

let typingDiv = null;

function typeWriterEffect(element, text, speed = 20) {
    const words = text.split(" ");
    let index = 0;

    function type() {
        if (index < words.length) {
            const formatted = formatMessage(words[index]);
            element.innerHTML += (index === 0 ? "" : " ") + formatted;
            index++;
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            setTimeout(type, speed);
        }
    }

    type();
}


let session_id = null;

window.onload = function () {
    messagesContainer.innerHTML = "";
    addMessage("Welcome! How can I help you today?", "assistant");
};

function createSessionID() {
    return "sess_" + Math.random().toString(36).substring(2, 10);
}

inputField.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {
    const text = inputField.value.trim();
    if (!text) return;

    if (!session_id) {
        const res = await fetch("/new_chat");
        const data = await res.json();
        session_id = data.session_id;
    }

    addMessage(text, "user");
    inputField.value = "";

    addTyping();

    try {
        const resp = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: session_id,
                user_input: text
            })
        });

        const data = await resp.json();
        removeTyping();

        if (data.orchestration_command) {
            addMessage("Processing request...", "assistant");
            await handleOrchestration(data.orchestration_command, text);
            return;
        }

        addMessage(data.response_text, "assistant");

    } catch (err) {
        removeTyping();
        addMessage("Server error, please try again.", "assistant");
    }
}

function addTyping() {
    typingDiv = document.createElement("div");
    typingDiv.className = "message-group assistant";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.innerText = "AI Assistant";

    const dots = document.createElement("div");
    dots.className = "message-text";
    dots.innerText = "...";

    content.appendChild(label);
    content.appendChild(dots);
    typingDiv.appendChild(content);

    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTyping() {
    if (typingDiv) typingDiv.remove();
    typingDiv = null;
}

async function handleOrchestration(cmd, user_text) {
    let step = cmd.replace("[[FLASK_CALL:", "").replace("]]", "");

    if (step === "VERIFY_KYC") {
        const customer_id = (user_text.match(/cust[\w\d]+/i) || [""])[0];

        const resp = await fetch("/orchestrate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                step: "VERIFY_KYC",
                session_id: session_id,
                customer_info: { customer_id }
            })
        });

        const data = await resp.json();

        if (data.status === "success") {
            addMessage(`KYC Verified for ${data.customer_data.name}`, "assistant");
            addMessage("How much loan amount would you like to apply for?", "assistant");
        } else {
            addMessage(data.message, "assistant");
        }
    }

    if (step === "UNDERWRITE") {
        let amt = user_text.match(/\d+/)?.[0];
        if (!amt) amt = prompt("Enter loan amount:");

        const resp = await fetch("/orchestrate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                step: "UNDERWRITE",
                session_id: session_id,
                customer_info: { loan_amount: amt }
            })
        });

        const data = await resp.json();

        if (data.worker_message)
            addMessage(data.worker_message, "assistant");

        if (data.email_message)
            addMessage(data.email_message, "assistant");
    }
}

function formatMessage(text) {
    return text
        .replace(/\n/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/^\s*[-*]\s+(.*)/gm, "• $1");
}

function addMessage(text, sender) {
    if (emptyState) emptyState.style.display = "none";

    const group = document.createElement("div");
    group.className = "message-group " + sender;

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("div");
    label.className = "message-label";
    label.innerText = sender === "user" ? "You" : "AI Assistant";

    const messageText = document.createElement("div");
    messageText.className = "message-text";

    content.appendChild(label);
    content.appendChild(messageText);
    group.appendChild(content);
    messagesContainer.appendChild(group);

    if (sender === "assistant") {
        typeWriterEffect(messageText, text, 35);
    } else {
        messageText.innerHTML = formatMessage(text);
    }

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

newChatBtn.addEventListener("click", async () => {
    const res = await fetch("/new_chat");
    const data = await res.json();
    session_id = data.session_id;
    messagesContainer.innerHTML = "";
    inputField.value = "";

    addMessage("Welcome! How can I help you today?", "assistant");
});
