document.getElementById('submit').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    const results = await window.electronAPI.sendQuery(query);
    document.getElementById('results').innerHTML = results.map(r => `
      <div class="result">
        <strong>${r.title}</strong><p>${r.body}</p>
      </div>
    `).join('');
  });
  