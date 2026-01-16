import { useState, useEffect } from "react";
import api from "../services/api";

function MeasureBuilder({ datasetId }) {
    const [measures, setMeasures] = useState([]);
    const [name, setName] = useState("");
    const [formula, setFormula] = useState("");
    const [previewData, setPreviewData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [columns, setColumns] = useState([]);

    useEffect(() => {
        if (!datasetId) return;
        loadData();
    }, [datasetId]);

    const loadData = async () => {
        try {
            const dsRes = await api.get(`/datasets/${datasetId}`);
            if (dsRes.data.measures) {
                setMeasures(JSON.parse(dsRes.data.measures));
            }
            const profRes = await api.get(`/datasets/${datasetId}/profile`);
            setColumns(profRes.data.columns);
        } catch (err) {
            console.error("Failed to load info", err);
        }
    };

    const fetchPreview = async (currentMeasures) => {
        setLoading(true);
        setError("");
        try {
            const res = await api.post(`/data-modeling/${datasetId}/preview`, { measures: currentMeasures });
            setPreviewData(res.data);
        } catch (err) {
            setError("Failed to preview measures. Check your formulas.");
        } finally {
            setLoading(false);
        }
    };

    const addMeasure = () => {
        if (!name || !formula) return;
        const newMeasures = [...measures, { name, formula }];
        setMeasures(newMeasures);
        setName("");
        setFormula("");
        fetchPreview(newMeasures);
    };

    const removeMeasure = (index) => {
        const newMeasures = measures.filter((_, i) => i !== index);
        setMeasures(newMeasures);
        fetchPreview(newMeasures);
    };

    const saveMeasures = async () => {
        setLoading(true);
        setError("");
        setSuccess("");
        try {
            await api.put(`/data-modeling/${datasetId}/save`, { measures: measures });
            setSuccess("Measures saved successfully!");
        } catch (err) {
            setError("Failed to save measures.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="measure-builder">
            <h2 style={{ marginBottom: "2rem" }}>Measure & Modeling Builder</h2>

            <div className="builder-panel card" style={{ padding: "1.5rem", marginBottom: "1.5rem" }}>
                <h4 style={{ marginBottom: "1rem" }}>Define New Measure</h4>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr auto", gap: "1rem", alignItems: "flex-end" }}>
                    <div className="form-group">
                        <label className="form-label">Measure Name</label>
                        <input type="text" className="form-input" value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Total_Profit" />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Formula (e.g. Sales - Cost)</label>
                        <input type="text" className="form-input" value={formula} onChange={e => setFormula(e.target.value)} placeholder="Use column names directly" />
                    </div>
                    <button className="btn btn-primary" onClick={addMeasure}>Add</button>
                </div>
                <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                    Available Columns: {columns.map(c => c.name).join(", ")}
                </div>
            </div>

            <div className="measures-list card" style={{ padding: "1.5rem", marginBottom: "1.5rem" }}>
                <h4 style={{ marginBottom: "1rem" }}>Custom Measures ({measures.length})</h4>
                {measures.length === 0 ? (
                    <p style={{ color: "var(--color-text-muted)" }}>No measures defined yet.</p>
                ) : (
                    <ul style={{ listStyle: "none", padding: 0 }}>
                        {measures.map((m, index) => (
                            <li key={index} style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                padding: "0.5rem",
                                borderBottom: "1px solid var(--border-color)",
                                background: 'rgba(255,255,255,0.05)',
                                marginBottom: '0.5rem',
                                borderRadius: '4px'
                            }}>
                                <span><strong>{m.name}</strong> = {m.formula}</span>
                                <button className="btn btn-outline" style={{ padding: '0.2rem 0.6rem', color: '#ff4444' }} onClick={() => removeMeasure(index)}>Remove</button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <div className="actions" style={{ marginBottom: "1.5rem", display: 'flex', gap: '1rem' }}>
                <button onClick={saveMeasures} disabled={loading} className="btn btn-primary">
                    {loading ? "Saving..." : "Save Measures"}
                </button>
                <button onClick={() => fetchPreview(measures)} className="btn btn-secondary">Refresh Preview</button>
            </div>

            {error && <div className="message-box message-error">{error}</div>}
            {success && <div className="message-box message-success">{success}</div>}

            <div className="preview-section card" style={{ padding: "1.5rem", overflowX: 'auto' }}>
                <h4 style={{ marginBottom: "1rem" }}>Data Preview with Measures</h4>
                {previewData ? (
                    <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: 'var(--color-background-surface)' }}>
                                {previewData.columns.slice(-5).map(col => ( // Show last 5 cols which include new measures
                                    <th key={col} style={{ padding: '0.8rem', textAlign: 'left', borderBottom: '2px solid var(--border-color)' }}>{col}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {previewData.data.slice(0, 5).map((row, i) => (
                                <tr key={i} style={{ borderBottom: '1px solid var(--border-color)' }}>
                                    {previewData.columns.slice(-5).map(col => (
                                        <td key={col} style={{ padding: '0.8rem' }}>{row[col]}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p style={{ color: "var(--color-text-muted)" }}>No preview available.</p>
                )}
            </div>
        </div>
    );
}

export default MeasureBuilder;
