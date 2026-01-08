import { useState } from 'react'
import { useEffect } from "react";

import api from "./services/api";
import './App.css'
import DatasetUpload from "./components/DatasetUpload";
import DatasetProfile from "./components/DatasetProfile";
import ChartBuilder from "./components/ChartBuilder";
import Dashboard from './components/Dashboard';
import boclogo from './assets/boclogo.png';

function App() {
  const [datasetId, setDatasetId] = useState(null);

  useEffect(() => {
    api.get("/")
      .then(res => console.log(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <img src={boclogo} alt="BOC Logo" style={{ maxWidth: "200px", marginBottom: "20px" }} />
      <h1>BOC BI Analytics Platform</h1>

      <DatasetUpload onUploadSuccess={setDatasetId} />

      {datasetId && (
        <>
          <p><strong>Dataset ID:</strong> {datasetId}</p>
          <DatasetProfile datasetId={datasetId} />
          <ChartBuilder datasetId={datasetId} />
          <Dashboard datasetId={datasetId} />
        </>
      )}
    </div>
  )
}

export default App
