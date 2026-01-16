import { useState, useEffect } from "react";
import api from "../services/api";
import TransformPanel from "./TransformPanel";

function DataPreparation({ datasetId }) {
    const [steps, setSteps] = useState([]);
    const [previewData, setPreviewData] = useState(null);
    const [columns, setColumns] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    useEffect(() => {
        if (!datasetId) return;
        loadDatasetInfo();
    }, [datasetId]);

    const loadDatasetInfo = async () => {
        try {
            const res = await api.get(`/datasets/${datasetId}/profile`);
            setColumns(res.data.columns);

            // Try to load existing transformations if they exist in dataset metadata
            // In a real app we'd have a specific GET for this or it would be in the profile
            // For now let's assume we fetch them when mounting
            const dsRes = await api.get(`/datasets/${datasetId}`);
            if (dsRes.data.transformations) {
                setSteps(JSON.parse(dsRes.data.transformations));
            }
        } catch (err) {
            console.error("Failed to load dataset info", err);
        }
    };

    const fetchPreview = async (currentSteps) => {
        setLoading(true);
        setError("");
        try {
            const res = await api.post(`/data-prep/${datasetId}/preview`, { transformations: currentSteps });
            setPreviewData(res.data);
            // Update columns based on preview if they changed (e.g. rename or drop)
            if (res.data.columns) {
                // Map strings to {name: s} for consistency with profile
                setColumns(res.data.columns.map(c => typeof c === 'string' ? { name: c } : c));
            }
        } catch (err) {
            setError("Failed to preview transformations. Check your steps and formulas.");
        } finally {
            setLoading(false);
        }
    };

    const addStep = (step) => {
        const newSteps = [...steps, step];
        setSteps(newSteps);
        fetchPreview(newSteps);
    };

    const removeStep = (index) => {
        const newSteps = steps.filter((_, i) => i !== index);
        setSteps(newSteps);
        fetchPreview(newSteps);
    };

    const saveTransformations = async () => {
        setLoading(true);
        setError("");
        setSuccess("");
        try {
            await api.put(`/data-prep/${datasetId}/save`, { transformations: steps });
            setSuccess("Transformations saved successfully!");
        } catch (err) {
            setError("Failed to save transformations.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="data-preparation">
            <h2 style={{ marginBottom: "2rem" }}>Data Preparation</h2>

            <TransformPanel onAddStep={addStep} columns={columns} />

            <div className="steps-list card" style={{ padding: "1.5rem", marginBottom: "1.5rem" }}>
                <h4 style={{ marginBottom: "1rem" }}>Applied Steps ({steps.length})</h4>
                {steps.length === 0 ? (
                    <p style={{ color: "var(--color-text-muted)" }}>No transformations applied yet.</p>
                ) : (
                    <ul style={{ listStyle: "none", padding: 0 }}>
                        {steps.map((step, index) => (
                            <li key={index} style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                padding: "0.5rem",
                                borderBottom: "1px solid var(--border-color)",
                                borderRadius: '4px',
                                background: 'rgba(255,255,255,0.05)',
                                marginBottom: '0.5rem'
                            }}>
                                <span>
                                    <strong>{step.type.toUpperCase()}</strong>: {JSON.stringify(step.params)}
                                </span>
                                <button className="btn btn-outline" style={{ padding: '0.2rem 0.6rem', color: '#ff4444' }} onClick={() => removeStep(index)}>Remove</button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <div className="actions" style={{ marginBottom: "1.5rem", display: 'flex', gap: '1rem' }}>
                <button onClick={saveTransformations} disabled={loading} className="btn btn-primary">
                    {loading ? "Saving..." : "Apply & Save to Dataset"}
                </button>
                <button onClick={() => fetchPreview(steps)} className="btn btn-secondary">Refresh Preview</button>
            </div>

            {error && <div className="message-box message-error">{error}</div>}
            {success && <div className="message-box message-success">{success}</div>}

            <div className="preview-section card" style={{ padding: "1.5rem", overflowX: 'auto' }}>
                <h4 style={{ marginBottom: "1rem" }}>Data Preview (Post-Transformation)</h4>
                {loading && <p>Loading preview...</p>}
                {previewData ? (
                    <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: 'var(--color-background-surface)' }}>
                                {previewData.columns.map(col => (
                                    <th key={col} style={{ padding: '0.8rem', textAlign: 'left', borderBottom: '2px solid var(--border-color)' }}>{col}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {previewData.data.slice(0, 10).map((row, i) => (
                                <tr key={i} style={{ borderBottom: '1px solid var(--border-color)' }}>
                                    {previewData.columns.map(col => (
                                        <td key={col} style={{ padding: '0.8rem' }}>{row[col]}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p style={{ color: "var(--color-text-muted)" }}>No preview available. Add transformations or click Refresh.</p>
                )}
            </div>
        </div>
    );
}

export default DataPreparation;
