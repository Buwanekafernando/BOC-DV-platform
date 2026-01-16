import { useState, useEffect } from "react";
import api from "../services/api";

function TransformPanel({ onAddStep, columns }) {
    const [type, setType] = useState("rename");
    const [params, setParams] = useState({});

    const handleAdd = () => {
        onAddStep({ type, params });
        setParams({});
    };

    return (
        <div className="transform-panel card" style={{ padding: "1.5rem", marginBottom: "1.5rem" }}>
            <h4 style={{ marginBottom: '1rem' }}>Add Transformation Step</h4>
            <div className="form-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                <div className="form-group">
                    <label className="form-label">Step Type</label>
                    <select value={type} onChange={e => { setType(e.target.value); setParams({}); }} className="form-select">
                        <option value="rename">Rename Column</option>
                        <option value="drop">Drop Column</option>
                        <option value="type_convert">Change Type</option>
                        <option value="filter">Filter Rows</option>
                        <option value="derived_column">Derived Column</option>
                    </select>
                </div>

                {type === "rename" && (
                    <>
                        <div className="form-group">
                            <label className="form-label">Target Column</label>
                            <select onChange={e => setParams({ ...params, target: e.target.value })} className="form-select">
                                <option value="">Select Column</option>
                                {columns.map(c => <option key={c.name} value={c.name}>{c.name}</option>)}
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">New Name</label>
                            <input
                                type="text"
                                className="form-input"
                                onChange={e => setParams({ columns: { [params.target]: e.target.value } })}
                            />
                        </div>
                    </>
                )}

                {type === "drop" && (
                    <div className="form-group">
                        <label className="form-label">Column to Drop</label>
                        <select onChange={e => setParams({ columns: [e.target.value] })} className="form-select">
                            <option value="">Select Column</option>
                            {columns.map(c => <option key={c.name} value={c.name}>{c.name}</option>)}
                        </select>
                    </div>
                )}

                {type === "type_convert" && (
                    <>
                        <div className="form-group">
                            <label className="form-label">Column</label>
                            <select onChange={e => setParams({ ...params, column: e.target.value })} className="form-select">
                                <option value="">Select Column</option>
                                {columns.map(c => <option key={c.name} value={c.name}>{c.name}</option>)}
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">New Type</label>
                            <select onChange={e => setParams({ ...params, dtype: e.target.value })} className="form-select">
                                <option value="">Select Type</option>
                                <option value="numeric">Numeric</option>
                                <option value="datetime">DateTime</option>
                                <option value="str">String</option>
                            </select>
                        </div>
                    </>
                )}

                {type === "filter" && (
                    <>
                        <div className="form-group">
                            <label className="form-label">Column</label>
                            <select onChange={e => setParams({ ...params, column: e.target.value })} className="form-select">
                                <option value="">Select Column</option>
                                {columns.map(c => <option key={c.name} value={c.name}>{c.name}</option>)}
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Operator</label>
                            <select onChange={e => setParams({ ...params, operator: e.target.value })} className="form-select">
                                <option value="eq">Equals</option>
                                <option value="ne">Not Equals</option>
                                <option value="gt">Greater Than</option>
                                <option value="lt">Less Than</option>
                                <option value="contains">Contains</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Value</label>
                            <input
                                type="text"
                                className="form-input"
                                onChange={e => setParams({ ...params, value: e.target.value })}
                            />
                        </div>
                    </>
                )}

                {type === "derived_column" && (
                    <>
                        <div className="form-group">
                            <label className="form-label">New Column Name</label>
                            <input
                                type="text"
                                className="form-input"
                                onChange={e => setParams({ ...params, name: e.target.value })}
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Formula (e.g. Sales * 0.1)</label>
                            <input
                                type="text"
                                className="form-input"
                                onChange={e => setParams({ ...params, formula: e.target.value })}
                            />
                        </div>
                    </>
                )}

                <div className="form-group" style={{ display: 'flex', alignItems: 'flex-end' }}>
                    <button onClick={handleAdd} className="btn btn-primary" style={{ width: '100%' }}>Add Step</button>
                </div>
            </div>
        </div>
    );
}

export default TransformPanel;
