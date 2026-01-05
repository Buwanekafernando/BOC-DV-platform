import { useState } from "react";
import ChartBuilder from "./ChartBuilder";

function Dashboard({ datasetId }) {
    const [charts, setCharts] = useState([]);

    const addChart = () => {
        setCharts([...charts, { id: Date.now() }]);
    };

    return (
        <div style={{ marginTop: "40px" }}>
            <h2>Dashboard</h2>

            <button onClick={addChart}>➕ Add Chart</button>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(2, 1fr)",
                    gap: "30px",
                    marginTop: "20px"
                }}
            >
                {charts.map(chart => (
                    <div key={chart.id} style={{ border: "1px solid #ccc", padding: "20px" }}>
                        <ChartBuilder datasetId={datasetId} />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Dashboard;