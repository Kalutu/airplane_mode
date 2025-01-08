import frappe
from frappe.utils import nowdate
from frappe import _

def update_expired_contracts():
    """
    Updates the shop status to 'Expired' if the contract has expired.
    """
    # Fetch contracts where expiry date is in the past
    expired_contracts = frappe.get_all(
        "Contract",
        filters={"contract_expiry_date": ["<", nowdate()]},
        fields=["name", "shop"]
    )

    for contract in expired_contracts:
        # Fetch the shop associated with the contract
        shop = frappe.get_doc("Shop", contract.shop)

        # Update the shop's status to Expired
        shop.status = "Expired"
        shop.save(ignore_permissions=True)

        # Log the update
        frappe.logger().info(f"Shop '{shop.name}' marked as Expired due to contract '{contract.name}' expiry.")

def send_rent_reminders():
    """Send monthly rent reminders to tenants if reminders are enabled."""
    if not is_rent_reminder_enabled():
        frappe.log_error("Rent reminders are disabled in settings.", "Rent Reminder Skipped")
        return

    tenants = frappe.db.sql(
        """
        SELECT
            t.name, t.email, c.shop
        FROM
            `tabTenant` t
        JOIN
            `tabContract` c ON c.tenant = t.name
        WHERE
            c.contract_expiry_date >= %s
        """,
        nowdate(),
        as_dict=True,
    )

    for tenant in tenants:
        if not tenant.email:
            continue
        
        subject = _("Rent Due Reminder")
        message = frappe.render_template(
            """
            <p>Dear {{ tenant.name }},</p>
            <p>This is a friendly reminder that your rent</strong> 
            for the shop <strong>{{ tenant.shop }}</strong> is due for this month.</p>
            <p>Kindly make your payment promptly to avoid penalties.</p>
            <p>Thank you,</p>
            <p>The Airport Management Team</p>
            """,
            {"tenant": tenant},
        )

        frappe.sendmail(
            recipients=tenant.email,
            subject=subject,
            message=message,
        )

def update_ticket_gate_numbers(flight, new_gate_number):
    """
    Updates gate numbers for all tickets associated with a flight.

    Args:
        flight (str): The name of the Flight whose tickets need to be updated.
        new_gate_number (str): The new gate number to set in the tickets.
    """
    try:
        # Fetch all tickets linked to the flight
        tickets = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": flight},
            fields=["name", "gate_number"],
        )

        for ticket in tickets:
            # Update gate number for each ticket
            frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", new_gate_number)
        
        frappe.db.commit() 
        frappe.logger().info(f"Updated gate numbers for tickets of flight {flight}")
    except Exception as e:
        frappe.logger().error(f"Error updating tickets for flight {flight}: {str(e)}")
        frappe.throw(_("Failed to update gate numbers for tickets."))
