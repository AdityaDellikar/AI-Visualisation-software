import React, { useState } from "react";
import { API_BASE_URL } from "../config";

const ExcelUploader = ({ onStart, onResult, onError }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [fileName, setFileName] = useState("");

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setIsUploading(true);
    onStart?.();

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Analyze failed: ${response.status}`);
      }

      const json = await response.json();
      onResult(json);
    } catch (err) {
      console.error("Upload failed:", err);
      onError?.();
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
          ⏳ Uploading & analyzing…
        </div>
      )}
    </div>
  );
};

export default ExcelUploader;