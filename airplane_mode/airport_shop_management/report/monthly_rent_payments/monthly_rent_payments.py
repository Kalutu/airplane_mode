import frappe
from frappe import _
from frappe.utils import get_first_day, get_last_day, nowdate


def execute(filters: dict | None = None):
    """Return columns and data for the report."""
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns() -> list[dict]:
    """Return columns for the report."""
    return [
        {
            "label": _("Month"),
            "fieldname": "month",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Tenant"),
            "fieldname": "tenant",
            "fieldtype": "Link",
            "options": "Tenant",
            "width": 200,
        },
        {
            "label": _("Total Rent Collected"),
            "fieldname": "total_rent",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": _("Number of Payments"),
            "fieldname": "payment_count",
            "fieldtype": "Int",
            "width": 120,
        },
    ]


def get_data(filters: dict | None) -> list[dict]:
    """Return data for the report."""
    if not filters:
        filters = {}

    # Use today's date as default for the report
    today = nowdate()
    start_date = filters.get("start_date", get_first_day(today))
    end_date = filters.get("end_date", get_last_day(today))

    data = frappe.db.sql(
        """
        SELECT 
            DATE_FORMAT(payment_date, '%%Y-%%m') AS month,
            tenant,
            SUM(payment_amount) AS total_rent,
            COUNT(name) AS payment_count
        FROM `tabRent Payment`
        WHERE payment_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY month, tenant
        ORDER BY month, tenant
        """,
        {"start_date": start_date, "end_date": end_date},
        as_dict=True
    )

    return data
