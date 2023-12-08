// Copyright (c) 2023, Narayanan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Register Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": "",
			"reqd": 1,
			"width": "100px",
			"onchange": "updateToDate"
		},
		{
			"fieldname": "to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": "",
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": "100px",
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "100px",
		},
		{
			"fieldname":"designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			"width": "100px",
		}


	]

	
};
