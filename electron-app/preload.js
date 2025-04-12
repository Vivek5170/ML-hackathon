const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendQuery: (query) => ipcRenderer.invoke('query-message', query)
});
