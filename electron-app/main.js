const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
  const win = new BrowserWindow({
    width: 1800,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

// Handle query from frontend
ipcMain.handle('query', async (event, query) => {
  return new Promise((resolve, reject) => {
    const py = spawn('python', ['../python-core/main_bot.py', query]);

    let output = '';
    py.stdout.on('data', (data) => output += data.toString());
    py.stderr.on('data', (err) => console.error('stderr:', err.toString()));
    py.on('close', () => resolve(output.trim()));
  });
});
