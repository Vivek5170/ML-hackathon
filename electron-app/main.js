const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow () {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}

ipcMain.handle('query-message', async (event, query) => {
  return new Promise((resolve, reject) => {
    const py = spawn('python', ['python-core/main_bot.py']);
    py.stdin.write(JSON.stringify({ query }));
    py.stdin.end();

    let data = '';
    py.stdout.on('data', chunk => data += chunk);
    py.stderr.on('data', err => console.error(err.toString()));
    py.on('close', () => resolve(JSON.parse(data)));
  });
});

app.whenReady().then(createWindow);
