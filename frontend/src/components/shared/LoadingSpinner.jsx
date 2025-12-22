const LoadingSpinner = ({ message = "Procesando..." }) => {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
        <p className="loading-message">{message}</p>
      </div>
    );
  };
  
  export default LoadingSpinner;