const LoadingSpinner = () => {
  return (
    <div className="col-12 mx-auto my-5 text-center">
      <div className="loading-indicator d-inline-block">
        <div className="dot" />
        <div className="dot" />
        <div className="dot" />
      </div>
    </div>
  );
};

export default LoadingSpinner;
