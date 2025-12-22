const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-brand">
          <span className="footer-logo">🎙️</span>
          <span className="footer-name">VoiceNotes.AI</span>
        </div>

        <div className="footer-links">
          <a href="https://github.com/antuansabe" target="_blank" rel="noopener noreferrer" className="footer-link">GitHub</a>
        </div>

        <div className="footer-credit">
          <p>Built with ❤️ by Antonn • Powered by Azure AI</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
