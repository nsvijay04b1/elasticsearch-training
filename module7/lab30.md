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

### Expected Output
When a user logs in from a country they have never visited before, the ML job will assign a high anomaly score. If that score exceeds 75, a Security Alert will be automatically generated.

💡 **Why?** Static threshold rules cannot detect "impossible travel" or brand-new behavior. Machine Learning automatically learns the baseline of "normal" for every user and flags deviations without manual configuration.
