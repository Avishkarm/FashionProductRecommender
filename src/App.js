import React, { useState } from 'react';
import Body from './components/Body';
import Header from './components/Header';
import './index.css';

function App() {
  const [searchText, setSearchText] = useState('');

  return (
    <div className="App">
      <Header setSearchText={setSearchText} />
      <Body searchText={searchText} />
    </div>
  );
}

export default App;
