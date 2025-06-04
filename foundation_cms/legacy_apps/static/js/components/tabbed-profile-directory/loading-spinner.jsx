import { getText } from "./locales";

const LoadingSpinner = () => {
  return (
    <div
      className="col-12 mx-auto my-5 text-center"
      aria-label={getText("Loading Icon")}
    >
      <div className="loading-indicator d-inline-block" aria-hidden="true">
        <div className="dot" />
        <div className="dot" />
        <div className="dot" />
      </div>
    </div>
  );
};

export default LoadingSpinner;
