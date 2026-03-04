# Lab 31: Importing Prebuilt Security Rules via API

## Objective
Learn how to use the Kibana Detection Engine API to automatically install the official Elastic Prebuilt Rules.

## Prerequisites
- Kibana v8.x is running.
- Your cluster credentials (username and password).

## Steps

### Step 1: Check Rule Status
Run this in **Dev Tools** to see if any prebuilt rules are already installed:
```json
GET /api/detection_engine/rules/_find?per_page=1
```

### Step 2: Install Prebuilt Rules via API
You can trigger the installation of hundreds of high-quality security rules with a single API call. Note that this can take a few minutes to process.

Run this in **Dev Tools**:
```json
PUT /api/detection_engine/rules/prebuilt
```

### Step 3: Verify Installation
Once the process completes, refresh your **Security** > **Rules** page. You should see the **Rule count** jump significantly (likely 800+).

**Example API Response for Step 2:**
```json
{
  "rules_installed": 842,
  "rules_updated": 0,
  "rules_missing": 0
}
```

### Expected Output
1. Go to **Security** > **Rules**.
2. Filter by **Tags: Elastic**.
3. You should see hundreds of rules populated, such as:
   - `Suspicious MS Office Child Process`
   - `Proxy Port Inbound Exception`
   - `Process Injection by unknown process`

### Summary Table for Testing

| Feature | Rule Type | Field to Watch |
| --- | --- | --- |
| **Brute Force** | Threshold | `source.ip` |
| **Malware Download** | EQL | `process.args` |
| **Data Theft** | ES|QL | `total_bytes` |
| **New Behavior** | ML | `Anomaly Score` |

💡 **Why?** Manually writing rules for every possible threat is impossible. Elastic's Security Intelligence team provides over 800 prebuilt rules that cover major security frameworks like MITRE ATT&CK and high-quality Security Information and Event Management (SIEM) detections.
