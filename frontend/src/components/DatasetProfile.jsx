import { useEffect, useState } from "react";
import api from "../services/api";

function DatasetProfile({ datasetId }) {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!datasetId) return;

        const fetchProfile = async () => {
            try {
                setLoading(true);
                const response = await api.get(`/profile/${datasetId}`);
                setProfile(response.data);
            } catch (err) {
                setError("Failed to load dataset profile");
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, [datasetId]);

    if (!datasetId) return null;
    if (loading) return <p>Loading dataset profile...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div style={{ marginTop: "30px" }}>
            <h3>Dataset Profile</h3>

            <table border="1" cellPadding="8">
                <thead>
                    <tr>
                        <th>Column Name</th>
                        <th>Data Type</th>
                        <th>Missing Values</th>
                    </tr>
                </thead>
                <tbody>
                    {profile.columns.map((col, index) => (
                        <tr key={index}>
                            <td>{col.name}</td>
                            <td>{col.type}</td>
                            <td>{col.missing}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DatasetProfile;
