import { useState } from "react";
import api from "../services/api";

function DatasetUpload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handleUpload = async () => {
        if (!file) {
            setMessage("Please select a CSV file");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setLoading(true);
            const response = await api.post("/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            setMessage("Upload successful!");
            onUploadSuccess(response.data.dataset_id);
        } catch (error) {
            setMessage(
                error.response?.data?.detail || "Upload failed"
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px", border: "1px solid #ccc" }}>
            <h3>Upload CSV Dataset</h3>

            <input
                type="file"
                accept=".csv"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <br /><br />

            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Uploading..." : "Upload"}
            </button>

            <p>{message}</p>
        </div>
    );
}

export default DatasetUpload;
