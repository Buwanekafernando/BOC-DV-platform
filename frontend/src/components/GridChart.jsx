import ChartBuilder from "./ChartBuilder";
import "../styles/grid.css";

function GridChart({ datasetId }) {
  return (
    <div style={{ border: "1px solid #ccc", height: "100%" }}>
      <div className="chart-header" style={{ cursor: "move", padding: "8px" }}>
        Chart
      </div>
      <ChartBuilder datasetId={datasetId} />
    </div>
  );
}

export default GridChart;
