import { useState } from "react";
import ChartBuilder from "./ChartBuilder";
import FilterPanel from "./FilterPanel";

function Dashboard({ datasetId }) {
    const [charts, setCharts] = useState([]);
    const [filters, setFilters] = useState({});

    const addChart = () => {
        setCharts([...charts, { id: Date.now() }]);
    };

    const dashboardState = {
        name: "Sales Overview",
        dataset_id: datasetId,
        filters: filters,
        charts: charts.map(c => ({
            chart_type: c.chartType,
            x_axis: c.xAxis,
            y_axis: c.yAxis,
            aggregation: c.aggregation
        })),
        layout: { columns: 2 }
    };

    const saveDashboard = async () => {
        await api.post("/dashboards", dashboardState);
        alert("Dashboard saved successfully");
    };



    return (
        <div style={{ marginTop: "40px" }}>
            <h2>Dashboard</h2>

            <FilterPanel filters={filters} setFilters={setFilters} />


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
                        <ChartBuilder
                            key={chart.id}
                            datasetId={datasetId}
                            filters={filters}
                        />
                    </div>
                ))}
            </div>

            <button onClick={saveDashboard}>Save Dashboard</button>
            <div id="dashboard-canvas">
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
                        <ChartBuilder
                            key={chart.id}
                            datasetId={datasetId}
                            filters={filters}
                        />
                    </div>
                ))}
                </div>
                <ExportButtons dashboardId={dashboardId} />
            </div>

        
        </div>
    );
}

export default Dashboard;