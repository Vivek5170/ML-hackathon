async function ask() {
  const query = document.getElementById('query').value;
  if (!query.trim()) return;
  
  const response = await window.chatbot.query(query);
  document.getElementById('output').innerText = response;
}

// Trigger `ask()` on Enter key press
document.getElementById('query').addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    ask();
  }
});
