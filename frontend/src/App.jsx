import { useState } from 'react'
import { useEffect } from "react";

import api from "./services/api";
import './App.css'
import DatasetUpload from "./components/DatasetUpload";
import DatasetProfile from "./components/DatasetProfile";
import ChartBuilder from "./components/ChartBuilder";

function App() {
  const [datasetId, setDatasetId] = useState(null);

  useEffect(() => {
    api.get("/")
      .then(res => console.log(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>BI Analytics Platform</h1>

      <DatasetUpload onUploadSuccess={setDatasetId} />

      {datasetId && (
        <>
          <p><strong>Dataset ID:</strong> {datasetId}</p>
          <DatasetProfile datasetId={datasetId} />
          <ChartBuilder datasetId={datasetId} />
        </>
      )}
    </div>
  )
}

export default App
