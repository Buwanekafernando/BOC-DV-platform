import api from "../services/api";
import { exportAsImage } from "../utils/exportImage";

function ExportButtons({ dashboardId }) {
  const exportPDF = () => {
    window.open(
      `${api.defaults.baseURL}/export/dashboard/${dashboardId}/pdf`,
      "_blank"
    );
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <button onClick={exportPDF}>📄 Export PDF</button>
      <button onClick={() => exportAsImage("dashboard-canvas")}>
        🖼 Export Image
      </button>
    </div>
  );
}

export default ExportButtons;
