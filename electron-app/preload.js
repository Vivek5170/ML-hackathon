const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('chatbot', {
  query: (input) => ipcRenderer.invoke('query', input)
});
