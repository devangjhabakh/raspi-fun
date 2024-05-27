// A webpage that allows a user to:
// 1. Upload a file and set a cron expression
// 2. Delete a file
// 3. List all files

import React, { useState } from 'react';
import './App.css';

function App() {
  const [cron, setCron] = useState('');
  const [file, setFile] = useState('');

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cron</h1>
        <form>
          <input
            type="text"
            placeholder="Cron expression"
            value={cron}
            name="cron"
            onChange={(e) => setCron(e.target.value)}
          />
          <input
            type="file"
            name="file"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button type="button" onClick={() => {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('cron', cron);
            fetch('http://localhost:8000/upload', { method: 'POST', body: formData});
            }}>Upload</button>
        </form>
      </header>
    </div>
  );
}

export default App;
