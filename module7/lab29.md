# Lab 29: Data Exfiltration Detection (ES|QL)

## Objective
Use the new **Elasticsearch Query Language (ES|QL)** to detect potential data exfiltration by identifying users who have uploaded an unusually high volume of data.

## Prerequisites
- Elasticsearch and Kibana v8.x are running (ES|QL is available in v8.11+).
- Index `logs-network-default` exists or will be created.

## Steps

### Step 1: Create the ES|QL Detection Rule
1. Navigate to **Security** > **Rules**.
2. Click **Create new rule**.
3. **Rule Type**: Select **ES|QL**.
4. **Define Query**: Enter the following ES|QL query:
   ```esql
   FROM logs-network*
   | STATS total_bytes = SUM(destination.bytes) BY source.ip, user.name
   | WHERE total_bytes > 500000000
   | SORT total_bytes DESC
   ```
5. **About Rule**:
   - **Name**: `Potential Data Exfiltration - High Outbound Traffic`
   - **Severity**: `High`
6. Click **Create and activate**.

### Step 2: Ingest Sample Data
Simulate a large file upload (600MB) by running this in **Dev Tools**:

```json
POST /logs-network-default/_doc
{
  "@timestamp": "2026-03-04T10:10:00Z",
  "source.ip": "10.0.0.5",
  "user.name": "v.kumar",
  "destination.bytes": 600000000,
  "destination.ip": "203.0.113.10"
}
```

### Expected Output
1. Navigate to **Security** > **Alerts**.
2. Click on the alert **Potential Data Exfiltration - High Outbound Traffic**.
3. In the flyout, look at the **ES|QL Result** table:
   - **source.ip**: `10.0.0.5`
   - **user.name**: `v.kumar`
   - **total_bytes**: `600,000,000` (~600MB)
4. Notice how the table exactly matches the `STATS` and `WHERE` logic from your rule.

💡 **Why?** ES|QL is significantly more powerful for detection logic because it allows you to perform calculations (like `SUM`) and filtering in a single, readable pipe-based query.
