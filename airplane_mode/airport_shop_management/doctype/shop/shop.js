// Copyright (c) 2025, Kalutu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
		if (!frm.doc.rent_amount) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Airplane Mode Settings",
				},
				callback: function (r) {
					if (r.message) {
						frm.set_value("rent_amount", r.message.default_rent_amount || 0);
					}
				},
			});
		}
	},
});
