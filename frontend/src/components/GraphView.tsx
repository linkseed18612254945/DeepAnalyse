import type { GraphResponse } from "../types";

interface Props {
  data: GraphResponse;
}

const TYPE_COLORS: Record<string, string> = {
  person: "#58a6ff",
  organization: "#f0883e",
  location: "#3fb950",
  event: "#bc8cff",
  legislation: "#f778ba",
  financial_instrument: "#d2a8ff",
};

export default function GraphView({ data }: Props) {
  const entityMap = new Map(data.entities.map((e) => [e.id, e]));

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>
        Knowledge Graph ({data.entities.length} entities,{" "}
        {data.relationships.length} relationships)
      </h2>

      <div style={styles.section}>
        <h3 style={styles.subheading}>Entities</h3>
        <div style={styles.grid}>
          {data.entities.map((e) => (
            <div key={e.id} style={styles.card}>
              <span
                style={{
                  ...styles.badge,
                  background: TYPE_COLORS[e.entity_type] || "#484f58",
                }}
              >
                {e.entity_type}
              </span>
              <strong style={styles.entityName}>{e.name}</strong>
              {e.description && (
                <p style={styles.desc}>{e.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {data.relationships.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.subheading}>Relationships</h3>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Source</th>
                <th style={styles.th}>Relationship</th>
                <th style={styles.th}>Target</th>
                <th style={styles.th}>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {data.relationships.map((r) => {
                const src = entityMap.get(r.source_entity_id);
                const tgt = entityMap.get(r.target_entity_id);
                return (
                  <tr key={r.id}>
                    <td style={styles.td}>{src?.name ?? r.source_entity_id}</td>
                    <td style={styles.td}>
                      <code style={styles.relType}>{r.relationship_type}</code>
                    </td>
                    <td style={styles.td}>{tgt?.name ?? r.target_entity_id}</td>
                    <td style={styles.td}>{r.confidence}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    background: "#161b22",
    border: "1px solid #30363d",
    borderRadius: 8,
    padding: 24,
  },
  heading: {
    margin: "0 0 20px",
    fontSize: 18,
    color: "#c9d1d9",
  },
  section: {
    marginBottom: 24,
  },
  subheading: {
    fontSize: 15,
    color: "#8b949e",
    margin: "0 0 12px",
    textTransform: "uppercase" as const,
    letterSpacing: 1,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
    gap: 12,
  },
  card: {
    background: "#0d1117",
    border: "1px solid #21262d",
    borderRadius: 6,
    padding: 12,
  },
  badge: {
    display: "inline-block",
    padding: "2px 8px",
    borderRadius: 10,
    fontSize: 11,
    color: "#fff",
    marginBottom: 6,
  },
  entityName: {
    display: "block",
    color: "#c9d1d9",
    fontSize: 14,
    marginBottom: 4,
  },
  desc: {
    margin: 0,
    fontSize: 12,
    color: "#8b949e",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse" as const,
    fontSize: 13,
  },
  th: {
    textAlign: "left" as const,
    padding: "8px 12px",
    borderBottom: "1px solid #30363d",
    color: "#8b949e",
    fontWeight: 600,
  },
  td: {
    padding: "8px 12px",
    borderBottom: "1px solid #21262d",
    color: "#c9d1d9",
  },
  relType: {
    background: "#21262d",
    padding: "2px 6px",
    borderRadius: 4,
    fontSize: 12,
    color: "#f0883e",
  },
};
