import React, { useState } from "react";

const API_BASE = process.env.REACT_APP_API_BASE_URL;

const ExcelUploader = ({ onStart, onResult, onError }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [fileName, setFileName] = useState("");

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setIsUploading(true);
    onStart?.(); // ✅ notify App that analysis started

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Analyze request failed");
      }

      const json = await response.json();
      onResult(json);
    } catch (err) {
      console.error("Upload failed:", err);
      onError?.();
      alert("⚠️ Failed to analyze the Excel file.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div
      style={{
        marginBottom: "30px",
        padding: "16px",
        border: "1px dashed #ccc",
        borderRadius: "10px",
        background: "#fafafa",
      }}
    >
      <label style={{ fontWeight: 600, display: "block", marginBottom: "8px" }}>
        Upload Excel file
      </label>

      <input
        type="file"
        accept=".xlsx,.xls"
        onChange={handleFileUpload}
        disabled={isUploading}
      />

      {fileName && (
        <div style={{ marginTop: "8px", fontSize: "13px", color: "#555" }}>
          📄 {fileName}
        </div>
      )}

      {isUploading && (
        <div style={{ marginTop: "10px", fontSize: "13px", color: "#666" }}>
          ⏳ Uploading & analyzing dataset…
        </div>
      )}
    </div>
  );
};

export default ExcelUploader;