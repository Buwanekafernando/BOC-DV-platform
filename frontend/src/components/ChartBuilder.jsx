import { useEffect, useState } from "react";
import {
    BarChart, Bar, LineChart, Line,
    XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";

import api from "../services/api";

function ChartBuilder({ datasetId }) {
    const [columns, setColumns] = useState([]);
    const [xAxis, setXAxis] = useState("");
    const [yAxis, setYAxis] = useState("");
    const [aggregation, setAggregation] = useState("sum");
    const [chartType, setChartType] = useState("bar");
    const [chartData, setChartData] = useState([]);

    useEffect(() => {
        if (!datasetId) return;

        api.get(`/profile/${datasetId}`).then(res => {
            setColumns(res.data.columns);
        });
    }, [datasetId]);

    const generateChart = async () => {
        const response = await api.post("/query", {
            dataset_id: datasetId,
            x_axis: xAxis,
            y_axis: yAxis,
            aggregation: aggregation
        });

        setChartData(response.data.data);
    };

    return (
        <div style={{ marginTop: "40px" }}>
            <h3>Chart Builder</h3>

            <label>Chart Type:</label>
            <select onChange={e => setChartType(e.target.value)}>
                <option value="bar">Bar</option>
                <option value="line">Line</option>
            </select>

            <br /><br />

            <label>X-Axis:</label>
            <select onChange={e => setXAxis(e.target.value)}>
                <option value="">Select</option>
                {columns.map(col => (
                    <option key={col.name} value={col.name}>{col.name}</option>
                ))}
            </select>

            <br /><br />

            <label>Y-Axis:</label>
            <select onChange={e => setYAxis(e.target.value)}>
                <option value="">Select</option>
                {columns.map(col => (
                    <option key={col.name} value={col.name}>{col.name}</option>
                ))}
            </select>

            <br /><br />

            <label>Aggregation:</label>
            <select onChange={e => setAggregation(e.target.value)}>
                <option value="sum">SUM</option>
                <option value="avg">AVG</option>
                <option value="count">COUNT</option>
                <option value="min">MIN</option>
                <option value="max">MAX</option>
            </select>

            <br /><br />

            <button onClick={generateChart}>Generate Chart</button>

            <br /><br />

            {chartData.length > 0 && chartType === "bar" && (
                <BarChart width={600} height={300} data={chartData}>
                    <CartesianGrid />
                    <XAxis dataKey="x" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="y" />
                </BarChart>
            )}

            {chartData.length > 0 && chartType === "line" && (
                <LineChart width={600} height={300} data={chartData}>
                    <CartesianGrid />
                    <XAxis dataKey="x" />
                    <YAxis />
                    <Tooltip />
                    <Line dataKey="y" />
                </LineChart>
            )}
        </div>
    );
}

export default ChartBuilder;

