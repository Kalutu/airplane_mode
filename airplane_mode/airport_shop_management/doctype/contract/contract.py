# Copyright (c) 2025, Kalutu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Contract(Document):
	def validate(self):
		shop = frappe.get_doc("Shop", self.shop)
		
		if shop.status != "Vacant":
			frappe.throw(f"Shop '{shop.name}' is currently not vacant. Unable to create a new contract.")

		# Update shop status to occupied and assign tenant
		shop.status = "Occupied"
		shop.tenant = self.tenant
		shop.save()
