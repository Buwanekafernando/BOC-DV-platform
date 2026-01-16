import { useEffect, useState } from "react";
import api from "../services/api";

function DatasetList({ onSelect }) {
    const [datasets, setDatasets] = useState([]);
    const [loading, setLoading] = useState(true);

    const handleDelete = async (id, e) => {
        e.stopPropagation(); // Prevent onSelect from firing
        if (window.confirm("Are you sure you want to delete this dataset?")) {
            try {
                await api.delete(`/datasets/${id}`);
                setDatasets(prev => prev.filter(d => d.id !== id));
            } catch (err) {
                console.error("Failed to delete dataset", err);
                alert("Failed to delete dataset. Please try again.");
            }
        }
    };

    useEffect(() => {
        api.get("/datasets/")
            .then(res => setDatasets(res.data))
            .catch(err => console.error("Failed to fetch datasets", err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <div className="dataset-list">
            {datasets.length > 0 ? (
                <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    {datasets.map(d => (
                        <li key={d.id} style={{ marginBottom: '8px' }}>
                            <button
                                onClick={() => onSelect(d.id)}
                                className="btn btn-secondary"
                                style={{ width: '100%', justifyContent: 'space-between', textAlign: 'left', display: 'flex', alignItems: 'center' }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <span style={{ marginRight: '8px', fontSize: '1.2rem' }}>📄</span>
                                    <div>
                                        <div style={{ fontWeight: '600' }}>{d.name}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Uploaded on {new Date(d.created_at || Date.now()).toLocaleDateString()}</div>
                                    </div>
                                </div>
                                <button
                                    onClick={(e) => handleDelete(d.id, e)}
                                    className="btn-icon"
                                    style={{ background: 'transparent', border: 'none', cursor: 'pointer', padding: '5px' }}
                                    title="Delete Dataset"
                                >
                                    🗑️
                                </button>
                            </button>
                        </li>
                    ))}
                </ul>
            ) : (
                <p style={{ color: 'var(--color-text-muted)', fontStyle: 'italic' }}>No uploaded datasets found.</p>
            )}
        </div>
    );
}

export default DatasetList;
