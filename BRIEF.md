# Set 2 — Image Intake

Objects created under `uploads/` in an S3 bucket should trigger a Lambda that stores object metadata in DynamoDB.

## Names the grader checks
Prefix: `h2-<your-id>-`.

| Resource | Exact name |
|---|---|
| ECR repository | `${prefix}-intake` |
| S3 bucket | `${prefix}-intake-<account-id>` |
| DynamoDB table | `${prefix}-intake` (hash key `object_key`) |
| IAM role | `${prefix}-intake-role` (permissions boundary required) |
| Log group | `/aws/lambda/${prefix}-intake` retention 14 days |
| Lambda | `${prefix}-intake` image, arm64 |

## Behaviour
- Bucket notification: `s3:ObjectCreated:*` with prefix `uploads/`.
- Handler writes an item with `object_key`, `size`, `content_type`, and `version`.
- Enable versioning, default encryption, and all four Block Public Access settings.

## Part A proof
`python3 tools/check_build.py --id <your-id>` uploads a test object and waits up to ~90s for the DynamoDB item.

## Part B
Fix the six issues in `crack-files/` and fill `FINDINGS.md`.
