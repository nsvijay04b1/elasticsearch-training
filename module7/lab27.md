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
To trigger the rule (Threshold > 10 in 5m), run this bulk command in **Dev Tools** to ingest 12 failed attempts at once:

```json
POST /_bulk
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:00Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:05Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:10Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:15Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:20Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:25Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:30Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:35Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:40Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:45Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:50Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
{ "index" : { "_index" : "logs-system.auth-default" } }
{ "@timestamp": "2026-03-04T10:00:55Z", "event.category": "authentication", "event.outcome": "failure", "source.ip": "192.168.1.50", "user.name": "admin" }
```

### Expected Output
1. Navigate to **Security** > **Alerts**.
2. Change the time range to **Last 15 minutes**.
3. You should see an alert:
   - **Rule**: `Brute Force Detection - Failed Logins`
   - **Reason**: `12 events triggered the threshold of 10`
   - **Source IP**: `192.168.1.50`

💡 **Why?** Threshold rules are the simplest way to catch high-volume attacks like brute force or port scanning. Grouping by `source.ip` ensures you catch the specific attacker, not just a general spike in Security Information and Event Management (SIEM) failures.
