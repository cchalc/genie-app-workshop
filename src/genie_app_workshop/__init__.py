# SPDX-License-Identifier: LicenseRef-Databricks
# Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE.
"""genie-app-workshop package. `table_name` is the template example; replace it with real code."""

__all__ = ["table_name"]


def table_name(catalog: str, schema: str, table: str) -> str:
    """Fully qualified Unity Catalog name."""
    for part, value in (("catalog", catalog), ("schema", schema), ("table", table)):
        if not value:
            raise ValueError(f"{part} is required")
    return f"{catalog}.{schema}.{table}"
