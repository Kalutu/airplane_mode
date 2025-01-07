# Copyright (c) 2025, Kalutu and contributors
# For license information, please see license.txt

import frappe, random
from frappe.model.document import Document


class AirplaneTicket(Document):
    def validate(self):
        self.check_seat_availability()
        self.set_seat()
        self.remove_duplicate_add_ons()
        self.calculate_total_amount()

    def check_seat_availability(self):
        flight = frappe.get_doc("Airplane Flight", self.flight)
        airplane = frappe.get_doc("Airplane", flight.airplane)
        airplane_capacity = airplane.capacity
        ticket_count = frappe.db.count("Airplane Ticket", {"flight": self.flight})
        
        if ticket_count >= airplane_capacity:
            frappe.throw(
                f"Cannot create a new ticket. The airplane capacity of {airplane_capacity} seats has been reached."
            )

    def set_seat(self):
        if not self.seat:
            random_number = random.randint(1, 100)  
            random_letter = random.choice("ABCDE")
            self.seat = f"{random_number}{random_letter}"

    def remove_duplicate_add_ons(self):
        unique_add_ons = {}
        clean_add_ons = []

        for addon in self.add_ons:
            if addon.item not in unique_add_ons:
                unique_add_ons[addon.item] = True
                clean_add_ons.append(addon)
        
        self.add_ons = clean_add_ons

    def calculate_total_amount(self):
        total_addons = 0

        if self.add_ons:
            for addon in self.add_ons:
                total_addons += addon.amount

        self.total_amount = self.flight_price  + total_addons

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("The ticket cannot be submitted because the status is not 'Boarded'.")




