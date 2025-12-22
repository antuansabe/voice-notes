const Navbar = ({ onGetStarted }) => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="brand-icon">🎙️</span>
          <span className="brand-name">VoiceNotes.AI</span>
          <span className="brand-badge">BETA</span>
        </div>

        <div className="navbar-links">
          <a href="#features" className="nav-link">Características</a>
          <a href="#how-it-works" className="nav-link">Cómo funciona</a>
          <a href="https://github.com/antuansabe" target="_blank" rel="noopener noreferrer" className="nav-link">
            GitHub
          </a>
          <button onClick={onGetStarted} className="nav-cta">
            Comenzar →
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
