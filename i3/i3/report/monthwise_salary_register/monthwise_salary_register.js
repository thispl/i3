// Copyright (c) 2023, Narayanan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthwise Salary Register"] = {
	"filters": [
			{
				"fieldname":"from_date",
				"label": __("From"),
				"fieldtype": "Date",
				"default": "",
				"reqd": 1,
				"width": "100px"
			},
			{
				"fieldname":"to_date",
				"label": __("To"),
				"fieldtype": "Date",
				"default": "",
				"reqd": 1,
				"width": "100px"
			},
			{
				"fieldname": "currency",
				"fieldtype": "Link",
				"options": "Currency",
				"label": __("Currency"),
				"default": erpnext.get_currency(frappe.defaults.get_default("Company")),
				"width": "50px"
			},
			{
				"fieldname":"company",
				"label": __("Company"),
				"fieldtype": "Link",
				"options": "Company",
				"default": "i3 Security Private Limited",
				"width": "100px",
				"reqd": 1
			},
			{
				"fieldname": "contractor",
				"fieldtype": "Link",
				"options": "Contractor",
				"label": __("Contractor"),
				"width": "50px"
			},
			{
				"fieldname":"docstatus",
				"label":__("Document Status"),
				"fieldtype":"Select",
				"options":["Draft", "Submitted", "Cancelled"],
				"default": "Draft",
				"width": "100px"
			}
		],
		onload: function (report) {
			var to_date = frappe.query_report.get_filter('to_date');
			to_date.refresh();
			var c = frappe.datetime.add_months(frappe.datetime.month_end())
			to_date.set_input(frappe.datetime.add_days(c))	
			var from_date = frappe.query_report.get_filter('from_date');
			from_date.refresh();
			var d = frappe.datetime.add_months(frappe.datetime.month_start(),)
			from_date.set_input(frappe.datetime.add_days(d))	
		}	
	
	};
	

	
