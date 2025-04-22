// const BASE_URL = "http://localhost:8000";
const BASE_URL = "https://12fc6727-87fb-4e2f-818c-e3745e878d4a-00-31aib82jicx3u.picard.replit.dev:8000/";

let token = null;
let selectedTopicId = null;
let currentUser = null; // Track the logged-in user

// Helper to make API requests
async function apiRequest(endpoint, method = "GET", body = null, isForm = false) {
    const headers = { "Content-Type": "application/json" };
    if (token) headers.Authorization = `Bearer ${token}`;
    if (isForm) headers["Content-Type"] = "application/x-www-form-urlencoded";
    const options = { method, headers };
    if (body) options.body = isForm ? body : JSON.stringify(body);
    const response = await fetch(`${BASE_URL}${endpoint}`, options);
    return response.ok ? response.json() : Promise.reject(await response.json());
}

// Update the logged-in username on the page
function updateUserDisplay() {
    const authSection = document.getElementById("auth-section");
    const usernameDisplay = document.getElementById("username-display");
    if (currentUser) {
        authSection.style.display = "none";
        usernameDisplay.textContent = `Logged in as: ${currentUser.username}`;
    } else {
        authSection.style.display = "flex";
        usernameDisplay.textContent = "";
    }
}

// Authentication handlers
document.getElementById("register-btn").onclick = async () => {
    const username = prompt("Username:");
    const email = prompt("Email:");
    const password = prompt("Password:");
    try {
        await apiRequest("/auth/register", "POST", { username, email, password });
        alert("Registration successful! You can now log in.");
    } catch (err) {
        alert(`Registration failed: ${err.error.message}`);
    }
};

document.getElementById("login-btn").onclick = async () => {
    const email = prompt("Email:");
    const password = prompt("Password:");
    try {
        const formData = new URLSearchParams();
        formData.append("username", email); // OAuth2PasswordRequestForm uses "username" for email
        formData.append("password", password);

        const response = await apiRequest("/auth/login", "POST", formData, true);
        token = response.token;
        currentUser = response.user;
        updateUserDisplay();
        document.getElementById("logout-btn").style.display = "inline-block";
        alert(`Login successful! Welcome, ${currentUser.username}.`);
        loadTopics();
    } catch (err) {
        alert(`Login failed: ${err.error.message}`);
    }
};

document.getElementById("logout-btn").onclick = async () => {
    try {
        await apiRequest("/auth/logout", "POST");
        token = null;
        currentUser = null;
        updateUserDisplay();
        document.getElementById("logout-btn").style.display = "none";
        alert("Logged out successfully.");
    } catch (err) {
        alert(`Logout failed: ${err.error.message}`);
    }
};

// Load topics
async function loadTopics() {
    try {
        const response = await apiRequest("/topics");
        const topicsList = document.getElementById("topics-list");
        topicsList.innerHTML = "";
        response.topics.forEach(topic => {
            const li = document.createElement("li");
            li.textContent = topic.title;
            li.onclick = () => selectTopic(topic.id);
            topicsList.appendChild(li);
        });
    } catch (err) {
        alert(`Failed to load topics: ${err.error.message}`);
    }
}

// Select topic and load comments
async function selectTopic(topicId) {
    selectedTopicId = topicId;
    try {
        const response = await apiRequest(`/topics/${topicId}/comments`);
        const commentsList = document.getElementById("comments-list");
        commentsList.innerHTML = "";
        response.comments.forEach(comment => {
            const li = document.createElement("li");
            li.textContent = `${comment.created_by.username}: ${comment.content}`;
            commentsList.appendChild(li);
        });
    } catch (err) {
        alert(`Failed to load comments: ${err.error.message}`);
    }
}

// Create a new topic
document.getElementById("new-topic-btn").onclick = async () => {
    const title = prompt("Topic Title:");
    const description = prompt("Topic Description:");
    try {
        await apiRequest("/topics", "POST", { title, description });
        loadTopics();
    } catch (err) {
        alert(`Failed to create topic: ${err.error.message}`);
    }
};

// Post a new comment
document.getElementById("post-comment-btn").onclick = async () => {
    const content = document.getElementById("new-comment-input").value;
    if (!selectedTopicId || !content) return;
    try {
        await apiRequest(`/topics/${selectedTopicId}/comments`, "POST", { content });
        document.getElementById("new-comment-input").value = "";
        selectTopic(selectedTopicId);
    } catch (err) {
        alert(`Failed to post comment: ${err.error.message}`);
    }
};

// Initial load
loadTopics();
updateUserDisplay();




