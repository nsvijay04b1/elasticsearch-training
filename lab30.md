# Lab 30: Anomaly Detection Rules (Machine Learning)

## Objective
Find "Improbable Access" (e.g., a user logging in from two different countries in a short window) using Machine Learning Anomaly Detection.

## Prerequisites
- **Elastic Platinum/Enterprise license** (or trial enabled) for Machine Learning features.
- Kibana v8.x is running.

## Steps

### Step 1: Create the ML Job
1. Navigate to **Machine Learning** > **Anomaly Detection**.
2. Click **Create job**.
3. Select the `logs-*` index pattern.
4. Use the **Rare** detector on the field `source.geo.country_iso_code` and correlate by `user.name`.
5. Name the job `rare_login_locations` and start the datafeed.

### Step 2: Create the Detection Rule
1. Navigate to **Security** > **Rules**.
2. Click **Create new rule**.
3. **Rule Type**: Select **Machine Learning**.
4. **Machine Learning Job**: Select the `rare_login_locations` job you created in Step 1.
5. **Anomaly Score Threshold**: Set to `75`.
6. **About Rule**:
   - **Name**: `Improbable Login Location Anomaly`
   - **Severity**: `Critical`
7. Click **Create and activate**.

### Step 3: Generate Baseline and Anomaly Data
ML needs a baseline of "normal" behavior before it can flag an anomaly. Run these commands in **Dev Tools**:

**1. Create "Normal" baseline (Logins from US):**
```json
POST /_bulk
{ "index" : { "_index" : "logs-rare-logins" } }
{ "@timestamp": "2026-03-04T08:00:00Z", "user.name": "alice", "source.geo.country_iso_code": "US" }
{ "index" : { "_index" : "logs-rare-logins" } }
{ "@timestamp": "2026-03-04T08:05:00Z", "user.name": "alice", "source.geo.country_iso_code": "US" }
{ "index" : { "_index" : "logs-rare-logins" } }
{ "@timestamp": "2026-03-04T08:10:00Z", "user.name": "alice", "source.geo.country_iso_code": "US" }
```

**2. Trigger the "Rare" Anomaly (First login from CN):**
```json
POST /logs-rare-logins/_doc
{
  "@timestamp": "2026-03-04T10:00:00Z",
  "user.name": "alice",
  "source.geo.country_iso_code": "CN"
}
```

### Expected Output
1. Navigate to **Machine Learning** > **Anomaly Detection** and view the **Anomaly Explorer**.
2. You will see a "Critical" (Red) anomaly for user `alice` because `CN` is a rare country for her baseline.
3. Now navigate to **Security** > **Alerts**. 
4. You should see an **Improbable Login Location Anomaly** alert with an anomaly score matching the ML job (e.g., 90+).

💡 **Why?** Static threshold rules cannot detect "impossible travel" or brand-new behavior. Machine Learning automatically learns the baseline of "normal" for every user and flags deviations without manual configuration.
