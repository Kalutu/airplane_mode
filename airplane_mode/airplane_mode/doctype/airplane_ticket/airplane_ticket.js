// Copyright (c) 2025, Kalutu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(
			__("Assign Seat"),
			function () {
				// Create a dialog to input the seat number
				const dialog = new frappe.ui.Dialog({
					title: "Select Seat",
					fields: [
						{
							label: "Seat Number",
							fieldname: "seat",
							fieldtype: "Data",
						},
					],
					primary_action_label: "Assign",
					primary_action(values) {
						// Set the Seat field in the form
						frm.set_value("seat", values.seat);

						// Close the dialog
						dialog.hide();

						// Optional: Save the form after setting the value
						frm.save();
					},
				});

				// Show the dialog
				dialog.show();
			},
			__("Actions")
		);
	},
});
