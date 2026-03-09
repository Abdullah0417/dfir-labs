SELECT
  accountid,
  count(*) AS finding_count
FROM gd_logs
GROUP BY accountid
ORDER BY finding_count DESC;
