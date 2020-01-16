import React from 'react';
import Ledger from './components/ledger';
import Nav from './components/nav'
import './App.css';

function App() {
  return (
    <div className="App">
      <header>
        <Nav />
      </header>
      <div>
        <Ledger />
      </div>
    </div>
  );
}

export default App;
