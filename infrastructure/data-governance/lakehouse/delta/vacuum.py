import logging


def deltaVacuum(spark, pathToTable: str, hours: int = None):
    """Vacuum a Delta Table

    Parameters
    ----------
    spark : SparkSession
        Spark session
    pathToTable : str
        Path to the Delta Table
    hours : int, optional
        Hours to keep, by default 7 days (Delta default)
    """
    from delta.tables import DeltaTable

    # Vacuum Delta Table
    if DeltaTable.isDeltaTable(spark, pathToTable):
        logging.info("Starting DeltaTable Vacuum")
        deltaTable = DeltaTable.forPath(spark, pathToTable)
        if hours:
            deltaTable.vacuum(hours)
        else:
            deltaTable.vacuum()
    else:
        raise TypeError(f"Table {pathToTable} is not a DeltaTable")
    pass


def deltaCompaction(
    spark,
    pathToTable: str,
):
    """Compact a Delta Table

    Parameters
    ----------
    spark : SparkSession
        Spark session
    pathToTable : str
        Path to the Delta Table
    """
    from delta.tables import DeltaTable

    # Compact Delta Table
    if DeltaTable.isDeltaTable(spark, pathToTable):
        logging.info("Starting DeltaTable Compaction")
        deltaTable = DeltaTable.forPath(spark, pathToTable)
        deltaTable.optimize().executeCompaction()
    else:
        raise TypeError(f"Table {pathToTable} is not a DeltaTable")
    pass


def deltaDetailDict(spark, pathToTable: str) -> dict:
    """
    Get the detail of a DeltaTable as a dict

    Parameters
    ----------
    spark : SparkSession
        SparkSession
    pathToTable : str
        Path to DeltaTable

    Returns
    -------
    dict
        Detail of DeltaTable
    """
    from delta.tables import DeltaTable

    detail_df = DeltaTable.forPath(spark, pathToTable).detail()
    detail_dict = detail_df.collect()[0].asDict()
    return detail_dict