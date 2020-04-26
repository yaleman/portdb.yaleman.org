# portdb.yaleman.org

## Zone and s3 bucket management

The main resources are configured with terraform:

 - s3 bucket
 - cloudflare DNS zone

Running terraform requires a bunch of environment variables

 - CLOUDFLARE_API_KEY
 - CLOUDFLARE_EMAIL
 - AWS_PROFILE (or AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID)


## Updating the s3 bucket

It is done through `hugo deploy`. You'll need AWS environment variables similar to the terraform run.