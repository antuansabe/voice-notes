const TechStack = () => {
  return (
    <section className="tech-stack-section">
      <div className="section-container">
        <div className="tech-stack-content">
          <h3 className="tech-stack-title">Powered by</h3>
          
          <div className="tech-logos">
            <div className="tech-item">
              <div className="tech-logo azure">☁️</div>
              <span>Azure Speech</span>
            </div>
            <div className="tech-item">
              <div className="tech-logo openai">🤖</div>
              <span>Azure OpenAI</span>
            </div>
            <div className="tech-item">
              <div className="tech-logo react">⚛️</div>
              <span>React</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechStack;
