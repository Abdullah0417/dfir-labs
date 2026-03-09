CREATE EXTERNAL TABLE IF NOT EXISTS gd_logs (
  schemaversion string,
  accountid string,
  region string,
  partition string,
  id string,
  arn string,
  type string,
  resource string,
  service string,
  severity string,
  createdat string,
  updatedat string,
  title string,
  description string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://lab07-guardduty-013052902523-us-east-1-findings/AWSLogs/013052902523/GuardDuty/'
TBLPROPERTIES ('has_encrypted_data'='true');
