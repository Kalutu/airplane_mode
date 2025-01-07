// Copyright (c) 2025, Kalutu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
		if (frm.doc.website) {
			const website_link = frm.doc.website;
			frm.add_web_link(website_link, "Visit Website");
		}
	},
});
