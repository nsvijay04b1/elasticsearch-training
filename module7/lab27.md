# Lab 27: Brute Force Detection (Threshold Rules)

## Objective
Learn how to create a Threshold Rule in the Elastic Security application to detect multiple failed login attempts from a single source IP.

## Prerequisites
- Elasticsearch and Kibana v8.x are running.
- Access to **Security** > **Rules** in Kibana.

## Steps

### Step 1: Navigate to Security Rules
1. Open the **Global Search** (top of Kibana) and type `Rules`.
2. Select **Security** > **Rules**.
3. Click **Create new rule** in the top right.

### Step 2: Configure the Threshold Rule
1. **Rule Type**: Select **Threshold**.
2. **Define Query**: Enter the following KQL query:
   ```kql
   event.category : "authentication" AND event.outcome : "failure"
   ```
3. **Threshold Settings**:
   - **Group by**: `source.ip`
   - **Count**: `> 10`
   - **Lookback window**: `5 minutes`
4. **About Rule**:
   - **Name**: `Brute Force Detection - Failed Logins`
   - **Severity**: `High`
   - **Interval**: `5 minutes`
5. Click **Create and activate**.

### Step 3: Generate Test Data
Paste and run the following command in **Dev Tools** at least 11 times (or use a simple script) to trigger the rule:

```json
POST /logs-system.auth-default/_doc
{
  "@timestamp": "2026-03-04T10:00:00Z",
  "event.category": "authentication",
  "event.outcome": "failure",
  "source.ip": "192.168.1.50",
  "user.name": "admin",
  "message": "Failed password for admin"
}
```

### Expected Output
After a few minutes, navigate to **Security** > **Alerts**. You should see an alert titled "Brute Force Detection - Failed Logins" flagging the IP `192.168.1.50`.

💡 **Why?** Threshold rules are the simplest way to catch high-volume attacks like brute force or port scanning. Grouping by `source.ip` ensures you catch the specific attacker, not just a general spike in Security Information and Event Management (SIEM) failures.
