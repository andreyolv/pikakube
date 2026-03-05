# Data Lake Cost Division by Project

## Problem:
- Lack of Granular Cost Allocation in Azure Storage Account: Azure Storage Accounts provide costs only at the storage account level, with no breakdown by individual directories or folders. This lack of granularity makes it difficult to track and allocate storage costs accurately for different projects, hindering visibility into the financial impact of each project’s data storage usage.
- Inadequate Project-Based Cost Tracking: With costs aggregated at the account level, stakeholders could not distinguish the costs associated with specific projects, making it challenging to manage budgets and allocate resources efficiently.
- Difficulty in Cost Allocation Based File Size: While allocating costs based on file size seems like a viable option, Azure Storage Accounts also incur additional transaction costs (e.g., read, write, and list operations). This makes it challenging to accurately allocate costs based solely on the size of the files, as transaction costs can vary significantly depending on the frequency and type of operations performed on the stored data. However, it remains a useful approximation, even if not perfectly accurate, for tracking costs since transaction metrics are not easily available to assist with cost allocation.

## Solution:
- Automated Cost Allocation: Designed and implemented an automated solution for dividing the data lake costs based on different projects, enabling cost tracking and reporting with accuracy.
- Cost Reporting Dashboards: Developed dashboard to visualize the Data Lake cost by project, providing stakeholders with insights into the financial status of each project within the data lake.
- Improved Budget Management: By linking storage usage to project costs, the solution helps teams make better decisions about resource allocation and budget planning. This promotes smarter storage management and reduces unnecessary expenses.

## Skills:
- DevOps
- FinOps

## Tools:
- Python
