https://azure.microsoft.com/en-us/pricing/details/storage/blobs/

https://stackoverflow.com/questions/77481664/physical-storage-differences-in-azure-storage-tiers

Only storage accounts that are configured for LRS, GRS, or RA-GRS support moving blobs to the archive tier. The archive tier isn't supported for ZRS, GZRS, or RA-GZRS accounts.

Rehydration priority:

- Standard priority: The rehydration request is processed in the order it was received and might take up to 15 hours to complete for objects under 10 GB in size.
- High priority: The rehydration request is prioritized over standard priority requests and might complete in less than one hour for objects under 10 GB in size.

How rehydratate:
- By copying it to a new blob in the hot, cool, or cold tier with the Copy Blob operation.
- By changing its tier from archive to hot, cool, or cold tier with the Set Blob Tier operation.

