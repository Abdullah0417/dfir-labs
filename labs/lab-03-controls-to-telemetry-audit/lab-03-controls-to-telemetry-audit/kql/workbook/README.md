# Lab 03 — Workbook KQL (Telemetry Coverage Dashboard)

This folder contains the KQL used by the **LAB03 — Telemetry Coverage Dashboard** workbook in Microsoft Sentinel (Azure portal).

## How to use
- Each `.kql` file maps to a specific **workbook part** (KPI tile, table, or chart).
- In the workbook editor: **Edit → select part → Query settings → paste KQL**.

## Executive section (stakeholder-friendly)

### 1) Coverage score KPI (last 24h)
**File:** `01_coverage_score.kql`  
**Purpose:** One-number view of audit/telemetry coverage.  
**Logic:** A signal only counts as **PASS** if it was observed across **all hosts** in the last 24h.  
**Suggested visualization:** **Tile**  
- Title: `Coverage score (last 24h)`  
- Big number: `CoveragePct`  
- Bottom: `Pass/Total + Last seen`

### 2) Endpoint reporting KPI (agent health)
**File:** `02_endpoints_reporting.kql`  
**Purpose:** “2/2 endpoints healthy” style KPI using Heartbeat.  
**Suggested visualization:** **Tile**  
- Big number: `Left` (e.g., `2/2`)  
- Subtitle: `Subtitle` (e.g., `endpoints healthy`)  
- Bottom: stale/missing breakdown + latest heartbeat

### 3) Logging tampering KPI (high risk)
**File:** `03_tampering_kpi.kql`  
**Purpose:** High-risk tampering signal summary (4719/1102).  
**Suggested visualization:** **Tile**  
- Big number: `Alerts`  
- Subtitle: `Status` (e.g., None detected / DETECTED)  
- Bottom: last seen + affected hosts OR “no events observed”

### 4) Top gaps table (missing telemetry per host)
**File:** `04_top_gaps.kql`  
**Purpose:** Business-readable punch list of missing signals per host.  
**Suggested visualization:** **Grid/Table**  
- Columns: Priority, Computer, Signal  
- Sorted by priority then host

### 5) Trend chart — failed logons (4625)
**File:** `05_trend_failed_logons.kql`  
**Purpose:** 24h failed logon trend with zero-filled buckets (prevents weird chart scaling).  
**Suggested visualization:** **Time chart**  
- Series: Failures by Computer  
- Step: 1 hour

### 6) Trend chart — Sysmon activity (EID 1 + 3)
**File:** `06_trend_sysmon_activity.kql`  
**Purpose:** 24h endpoint activity trend for Sysmon process + network telemetry.  
**Suggested visualization:** **Time chart**  
- Series: Events by Computer  
- Bucket: 1 hour

## Technical section (DFIR / IR drill-down)
Your deeper diagnostic queries (validation pack, raw event drill-down) live in:
- [`../validation/`](../validation/)

## Notes
- If chart queries return no results, it usually means the event didn’t occur in the lookback window (not a query bug).
- Keep workbook exports in: `..\workbooks\` (galleryTemplate JSON) and redact any identifiers before publishing.
