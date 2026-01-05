function FilterPanel({ filters, setFilters }) {
    return (
        <div style={{ marginBottom: "20px" }}>
            <h3>Filters</h3>

            <label>Category:</label>
            <input
                type="text"
                placeholder="e.g. Asia"
                onChange={e => setFilters({ ...filters, category: e.target.value })}
            />
        </div>
    );
}

export default FilterPanel;
