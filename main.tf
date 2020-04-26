terraform {
  backend "s3" {
    bucket = "yaleman-terraform-state"
    key    = "portdb.tfstate"
    region = "us-east-1"
  }
}

locals {
  domain_name = "portdb.yaleman.org"
  site_name = "portDb"
  aws_region = "us-east-1"

}


provider "aws" {
  region  = local.aws_region
}

resource aws_s3_bucket portdb_yaleman_org {
  bucket = local.domain_name
  acl    = "public-read"
  website {
    error_document = "index.html"
    index_document = "index.html"
    }
}

resource aws_s3_bucket_policy bucket_policy {
  bucket = aws_s3_bucket.portdb_yaleman_org.id

  policy = <<POLICY
{
  "Id": "Policy1573381116674",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1573381115327",
      "Action": [
        "s3:GetObject"
      ],
      "Effect": "Allow",
      "Resource": "${aws_s3_bucket.portdb_yaleman_org.arn}/*",
      "Principal": "*"
    }
  ]
}

POLICY
}

data cloudflare_zones yaleman_org {
  filter {
    name   = "yaleman.org"
    status = "active"
  }
}
resource cloudflare_record site_record {
  zone_id = data.cloudflare_zones.yaleman_org.zones[0].id
  name = "portdb.yaleman.org"
  type = "CNAME"
  value = "${local.domain_name}.s3-website-${local.aws_region}.amazonaws.com"
  ttl = 1
  proxied = true
}
