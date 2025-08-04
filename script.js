function addToChat(text, isUser = false) {
  const chatBox = document.getElementById("chat-box");
  const message = document.createElement("div");
  message.textContent = (isUser ? "🧑: " : "🤖: ") + text;
  chatBox.appendChild(message);
}

function sendQuestion() {
  const input = document.getElementById("user-input");
  const question = input.value.trim();
  if (!question) return;

  addToChat(question, true);
  input.value = "";

  fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  })
    .then((res) => res.json())
    .then((data) => {
      addToChat(data.response);
    })
    .catch((err) => {
      console.error(err);
      addToChat("Terjadi kesalahan.");
    });

    
}
