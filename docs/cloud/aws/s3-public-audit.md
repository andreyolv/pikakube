# Secure S3 Bucket Data Sharing via Partner IP Whitelisting

## Problem:
- Prevent Public Exposure: Establish a "Private by Design" storage architecture to ensure sensitive data is never accessible to the general public.
- Granular External Access: Define a strict security perimeter that allows only verified external partners to interact with specific S3 resources.
- End-to-End Auditability: Implement comprehensive logging to satisfy compliance requirements regarding who, when, and from where data is accessed.
- Automated Threat Detection: Create a mechanism to identify and log unauthorized connection attempts from non-whitelisted IP addresses.
- Infrastructure as Code Readiness: Build a scalable and repeatable policy model that can be applied to future buckets requiring similar partner integrations.

## Solution:
- Condition-Based Bucket Policies: Authored JSON policies using the aws:SourceIp condition key to restrict bucket access exclusively to the partner’s static CIDR blocks.
- Explicit Deny Logic: Implemented a "Deny" statement for all traffic originating outside the trusted IP range, which overrides any other permissive IAM permissions.
- CloudTrail Data Events Integration: Enabled granular logging of S3 Data Events (Object-level) to capture every GetObject operation for auditing.
- Access Monitoring & Visibility: Configured the environment to log both AccessDenied and Success events, providing a clear distinction between partner activity and external probes.
- Secure Transport Enforcement: Enforced SSL/TLS for all data in transit by requiring aws:SecureTransport within the bucket policy.
- Audit-Ready Architecture: Centralized log collection, enabling the security team to generate compliance reports and verify that data remained within the intended network boundary.
