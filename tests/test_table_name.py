# SPDX-License-Identifier: LicenseRef-Databricks
# Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE.
import pytest

from genie_app_workshop import table_name


def test_joins_the_three_parts() -> None:
    assert table_name("acme", "silver", "orders") == "acme.silver.orders"


@pytest.mark.parametrize("missing", ["catalog", "schema", "table"])
def test_rejects_a_missing_part(missing: str) -> None:
    parts = {"catalog": "acme", "schema": "silver", "table": "orders"} | {missing: ""}
    with pytest.raises(ValueError, match=missing):
        table_name(**parts)
