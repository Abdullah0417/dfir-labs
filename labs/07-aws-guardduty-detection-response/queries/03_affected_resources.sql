SELECT
  type,
  json_extract_scalar(resource, '$.resourceType') AS resource_type,
  coalesce(
    json_extract_scalar(resource, '$.instanceDetails.instanceId'),
    json_extract_scalar(resource, '$.accessKeyDetails.userName'),
    json_extract_scalar(resource, '$.s3BucketDetails[0].name')
  ) AS principal_or_resource,
  count(*) AS finding_count
FROM gd_logs
GROUP BY 1, 2, 3
ORDER BY finding_count DESC;
