async function ask() {
  const query = document.getElementById('query').value;
  const response = await window.chatbot.query(query);
  document.getElementById('output').innerText = response;
}
