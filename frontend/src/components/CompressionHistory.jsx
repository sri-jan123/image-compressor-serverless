import { useEffect, useState } from "react";
import axios from "axios";

function CompressionHistory() {

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

useEffect(() => {

  fetchHistory();

  const interval = setInterval(() => {
    fetchHistory();
  }, 3000); 

  return () => clearInterval(interval);

}, []);

  const fetchHistory = async () => {

    try {

      const response = await axios.get(
        "http://localhost:7071/api/getHistory"
      );

      setHistory(response.data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  const handleDownload = async (fileName) => {

    try {

      const response = await axios.get(
        `http://localhost:7071/api/downloadImage?fileName=${fileName}`
      );

      window.open(
        response.data.downloadUrl,
        "_blank"
      );

    } catch (error) {

      console.error(error);

      alert("Download failed.");

    }
  };

  return (

    <div className="history-container">

      <h2>Compression History</h2>

      {loading ? (

        <p>Loading...</p>

      ) : history.length === 0 ? (

        <p>No images processed yet.</p>

      ) : (

        <table className="history-table">

          <thead>

            <tr>
              <th>File Name</th>
              <th>Original Size</th>
              <th>Compressed Size</th>
              <th>Compression %</th>
              <th>Status</th>
              <th>Time</th>
              <th>Download</th>
            </tr>

          </thead>

          <tbody>

            {history.map((item) => (

              <tr key={item.id}>

                <td>{item.fileName}</td>

                <td>{item.originalSizeKB} KB</td>

                <td>{item.compressedSizeKB} KB</td>

                <td>{item.compressionPercentage}%</td>

                <td>{item.status}</td>

                <td>
                  {new Date(item.timestamp).toLocaleString()}
                </td>

                <td>

                  <button
                    className="download-btn"
                    onClick={() => handleDownload(item.fileName)}
                  >
                    Download
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>

  );
}

export default CompressionHistory;