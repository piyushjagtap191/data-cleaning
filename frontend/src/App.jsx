import React, { useState } from "react";
import axios from "axios";

const apiBase = "https://data-cleaning-j8b9.onrender.com";

function FileUploadSection({ label, endpoint, downloadName }) {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setDownloadUrl("");
  };
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post(`${apiBase}/upload/${endpoint}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setDownloadUrl(apiBase + res.data.download_url);
    } catch (err) {
      alert("Upload failed");
    }
    setLoading(false);
  };
  return (
    <div style={{ marginBottom: 32 }}>
      <h3>{label}</h3>
      <input type="file" accept=".xlsx,.xls" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading || !file} style={{ marginLeft: 8 }}>
        {loading ? "Processing..." : "Upload & Clean"}
      </button>
      {downloadUrl && (
        <a href={downloadUrl} download={downloadName} style={{ marginLeft: 16 }}>
          Download {downloadName}
        </a>
      )}
    </div>
  );
}

function App() {
  return (
    <div style={{ maxWidth: 600, margin: "40px auto", padding: 24, border: "1px solid #eee", borderRadius: 8, background: "#fafcff" }}>
      <h1>Excel Data Cleaner Dashboard</h1>
      <FileUploadSection label="SOH Containt" endpoint="soh" downloadName="Fresh_SOH.xlsx" />
      <FileUploadSection label="FR PO" endpoint="frpo" downloadName="Fresh_FR.xlsx" />
      <FileUploadSection label="SR Data" endpoint="srdata" downloadName="SR_Data.xlsx" />
      <div style={{marginTop:32, color:'#888', fontSize:14}}>
        <b>Instructions:</b> Upload each Excel file in its section. After processing, download the cleaned file.
      </div>
    </div>
  );
}

export default App
