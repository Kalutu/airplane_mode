import frappe

def execute():
    airplaneTickets = frappe.db.get_all("AirplaneTicket")

    for at in airplaneTickets:
        airplaneTicket = frappe.get_doc("AirplaneTicket",at)
        airplaneTicket.set_seat()
        airplaneTicket.save()

    frappe.db.commit()
