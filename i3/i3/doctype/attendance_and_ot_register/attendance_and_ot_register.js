// Copyright (c) 2023, Narayanan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance and OT Register', {
	start_date(frm) {
		frappe.call({
			method: 'i3.i3.doctype.attendance_and_ot_register.attendance_and_ot_register.get_end_date',
			args: {
				frequency: "Monthly",
				start_date: frm.doc.start_date
			},
			callback: function (r) {
				console.log("HI")
				if (r.message) {
					frm.set_value('end_date', r.message.end_date);
				}
			}
		});
	},
});
