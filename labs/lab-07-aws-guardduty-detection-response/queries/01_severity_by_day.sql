SELECT
  date(from_iso8601_timestamp(createdat)) AS finding_day,
  cast(severity AS double) AS severity_score,
  count(*) AS finding_count
FROM gd_logs
GROUP BY 1, 2
ORDER BY 1 DESC, 2 DESC;
