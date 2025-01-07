import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data()
    chart = get_chart(data)
    report_summary = get_report_summary(data)

    return columns, data, None, chart, report_summary


def get_columns():
    return [
        {"label": _("Airline"), "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]


def get_data():
    airlines = frappe.get_all("Airline", fields=["name"])
    data = []

    for airline in airlines:
        airplanes = frappe.get_all("Airplane", filters={"airline": airline.name}, fields=["name"])
        airplane_names = [airplane["name"] for airplane in airplanes]

        if not airplane_names:
            data.append({
                "airline": airline.name,
                "revenue": 0,
            })
            continue

        flights = frappe.get_all("Airplane Flight", filters={"airplane": ["in", airplane_names]}, fields=["name"])
        flight_names = [flight["name"] for flight in flights]

        if not flight_names:
            data.append({
                "airline": airline.name,
                "revenue": 0,
            })
            continue

        tickets = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": ["in", flight_names]},
            fields=["sum(total_amount) as revenue"]
        )
        revenue = tickets[0].get("revenue", 0) or 0

        data.append({
            "airline": airline.name,
            "revenue": revenue,
        })

    return data


def get_chart(data):
    labels = [row["airline"] for row in data]
    values = [row["revenue"] for row in data]

    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}],
        },
        "type": "donut",
        "height": 250,
    }


def get_report_summary(data):
    total_revenue = sum(row["revenue"] for row in data)

    return [
        {
            "value": total_revenue,
            "indicator": "Green",
            "label": _("Total Revenue"),
        }
    ]
