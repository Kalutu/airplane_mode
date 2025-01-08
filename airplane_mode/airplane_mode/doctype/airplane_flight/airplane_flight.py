# Copyright (c) 2025, Kalutu and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_save(self):
		if self.is_new() or not self.has_value_changed("gate_number"):
			return
		
		enqueue(
            method="airplane_mode.tasks.update_ticket_gate_numbers",
            queue="long",
            job_name=f"Update tickets for flight {self.name}",
            flight=self.name,
            new_gate_number=self.gate_number,
        )

	def before_submit(self):
		self.status = "Completed"
