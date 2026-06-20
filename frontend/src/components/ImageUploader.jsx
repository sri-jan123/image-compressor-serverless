import { useState } from "react";
import axios from "axios";
import { FaCloudUploadAlt, FaTrash } from "react-icons/fa";

const ImageUploader = () => {

  const [selectedImage, setSelectedImage] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const BASE_URL = import.meta.env.VITE_API_URL;

  const handleImageChange = (e) => {

    const file = e.target.files[0];

    if (file) {

      setSelectedImage({
        file,
        preview: URL.createObjectURL(file)
      });

      setResult(null);

    }
  };

  const removeImage = () => {

    setSelectedImage(null);
    setResult(null);

  };

  const pollImageStatus = (fileName) => {

    const interval = setInterval(async () => {

      try {

        const response = await axios.get(
          `${BASE_URL}/getimagestatus?fileName=${fileName}`
        );

        if (response.data.length > 0) {

          setResult(response.data[0]);

          setProcessing(false);

          clearInterval(interval);

        }

      } catch (error) {

        console.error(error);

      }

    }, 2000);

  };

  const handleUpload = async () => {

    if (!selectedImage) return;

    try {

      setUploading(true);

      const response = await axios.post(
        `${BASE_URL}/uploadimage`,
        selectedImage.file,
        {
          headers: {
            "Content-Type": selectedImage.file.type,
            filename: selectedImage.file.name
          }
        }
      );

      setUploading(false);
      setProcessing(true);

      pollImageStatus(response.data.fileName);

    } catch (error) {

      console.error(error);

      setUploading(false);

      alert("Upload failed");

    }
  };

  const handleDownload = async (fileName) => {

    try {

      const response = await axios.get(
        `${BASE_URL}/downloadImage?fileName=${fileName}`
      );

      window.open(response.data.downloadUrl, "_blank");

    } catch (error) {

      console.error(error);

      alert("Download failed");

    }

  };

  return (

    <div className="container">

      <div className="card">

        <h1>Image Compressor</h1>

        <p className="subtitle">
          Upload your image and optimize it instantly.
        </p>

        {!selectedImage ? (

          <label className="upload-box">

            <FaCloudUploadAlt className="upload-icon" />

            <h3>Drag & Drop Image</h3>

            <span>or click to browse</span>

            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
            />

          </label>

        ) : (

          <div className="preview-section">

            <img
              src={selectedImage.preview}
              alt="preview"
              className="preview-image"
            />

            <div className="file-details">

              <p>
                <strong>Name:</strong> {selectedImage.file.name}
              </p>

              <p>
                <strong>Size:</strong>{" "}
                {(selectedImage.file.size / 1024).toFixed(2)} KB
              </p>

            </div>

            <div className="button-group">

              <button
                className="upload-btn"
                onClick={handleUpload}
                disabled={uploading}
              >
                {uploading ? "Uploading..." : "Upload Image"}
              </button>

              <button
                className="delete-btn"
                onClick={removeImage}
              >
                <FaTrash />
              </button>

            </div>

          </div>

        )}

        {processing && (

          <div className="processing">

            <h3>Processing image...</h3>

          </div>

        )}

        {result && (

          <div className="history-container">

            <h2>Compression Result</h2>

            <table className="history-table">

              <thead>

                <tr>
                  <th>File Name</th>
                  <th>Original Size</th>
                  <th>Compressed Size</th>
                  <th>Compression %</th>
                  <th>Status</th>
                  <th>Download</th>
                </tr>

              </thead>

              <tbody>

                <tr>

                  <td>{result.fileName}</td>

                  <td>{result.originalSizeKB} KB</td>

                  <td>{result.compressedSizeKB} KB</td>

                  <td>{result.compressionPercentage}%</td>

                  <td>{result.status}</td>

                  <td>

                    <button
                      className="download-btn"
                      onClick={() =>
                        handleDownload(result.fileName)
                      }
                    >
                      Download
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

      </div>

    </div>

  );
};

export default ImageUploader;