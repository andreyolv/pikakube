# Dynamic Application Security Testing (DAST) with ZAP Proxy

## Problem:
- Lack of Runtime Security Testing: Applications are often tested for vulnerabilities only at the code level (SAST), neglecting potential security issues that can arise during runtime.
- Exposure to Web Application Attacks: Without dynamic testing, vulnerabilities such as SQL injection, XSS, and authentication flaws can remain undetected and exploitable.
- Manual Testing Inefficiencies: Manually testing for vulnerabilities in web applications is time-consuming and prone to human error.

## Solution:
- Automated DAST Scanning: Implemented OWASP ZAP Proxy to perform automated Dynamic Application Security Testing (DAST) against web applications during runtime.
- Security Testing Pipeline Integration: Integrated ZAP scans within CI/CD pipelines to ensure continuous testing of applications across development, staging, and production environments.
Standardized Testing Process: Established a structured approach to perform spidering, active scanning, and fuzzing to detect vulnerabilities such as: Injection Attacks (SQL Injection, Command Injection), Cross-Site Scripting (XSS), Authentication and Authorization Flaws, Security Misconfigurations, Sensitive Data Exposure.
- Reporting and Analysis: Configured ZAP to generate detailed reports with categorized findings, severity levels, and remediation recommendations.

## Skills:
- Security
- DevOps

## Tools:
- Github Actions
- OWASP ZAP Proxy
