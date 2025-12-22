import { useState } from 'react';

const EmailPreview = ({ emailData }) => {
  const [copied, setCopied] = useState(false);

  if (!emailData) return null;

  const copyToClipboard = () => {
    const emailText = `Para: ${emailData.para}\nAsunto: ${emailData.asunto}\n\n${emailData.cuerpo}`;
    navigator.clipboard.writeText(emailText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="email-preview">
      <h2>📧 Borrador de Email</h2>

      <div className="email-field">
        <label className="email-label">Para:</label>
        <input 
          type="text" 
          value={emailData.para || ''} 
          className="email-input"
          readOnly
        />
      </div>

      <div className="email-field">
        <label className="email-label">Asunto:</label>
        <input 
          type="text" 
          value={emailData.asunto || emailData.subject || ''} 
          className="email-input"
          readOnly
        />
      </div>

      <div className="email-field">
        <label className="email-label">Cuerpo:</label>
        <textarea 
          value={emailData.cuerpo || emailData.body || ''} 
          className="email-textarea"
          rows="12"
          readOnly
        />
      </div>

      <div className="email-actions">
        <button onClick={copyToClipboard} className="copy-button">
          {copied ? '✅ Copiado' : '📋 Copiar al portapapeles'}
        </button>
      </div>
    </div>
  );
};

export default EmailPreview;
