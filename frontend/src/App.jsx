import "./App.css";
import ImageUploader from "./components/ImageUploader";
import CompressionHistory from "./components/CompressionHistory";

function App() {
  return (
    <div className="app">
      <ImageUploader />
      <CompressionHistory/>
    </div>
  );
}

export default App;