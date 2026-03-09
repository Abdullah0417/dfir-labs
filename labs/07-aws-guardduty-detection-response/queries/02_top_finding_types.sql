SELECT
  type,
  count(*) AS finding_count
FROM gd_logs
GROUP BY type
ORDER BY finding_count DESC
LIMIT 25;
