# Set 2 - Image Intake. Write your infrastructure here.
#
# TODO ECR repository         ${local.prefix}-intake
# TODO S3 bucket              ${local.prefix}-intake-${local.account_id}
# TODO DynamoDB table         ${local.prefix}-intake
# TODO IAM role + policy      ${local.prefix}-intake-role (permissions_boundary!)
# TODO CloudWatch log group   /aws/lambda/${local.prefix}-intake
# TODO Lambda function        ${local.prefix}-intake (Image, arm64)
# TODO S3 -> Lambda notify    prefix uploads/
