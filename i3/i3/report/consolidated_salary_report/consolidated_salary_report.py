# Copyright (c) 2023, Narayanan and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns=get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = []
    columns += [
        _("Employee") + ":Link/Purchase Order:110",
        _("Employee Name") + ":Data:100",
        _("Date Of Birth") + ":Data:100",
        _("Date Of Joining") + ":Data:100",
        _("Company") + ":Data:100",
        _("Department") + ":Data:100",
        _("From Date") + ":Data:110",
        _("To Date") + ":Data:100",
        _("Bank Name") + ":Data:100",
        _("Bank A/C No") + ":Data:100",
        _("IFSC Code") + ":Data:100",
        _("Bank Branch") + ":Data:100",
        _("UAN No") + ":Data:100",
        _("ESI No") + ":Data:100",
        _("Payment Days") + ":Data:100",
        _("Basic") + ":Data:100",
        _("House Rent Allowance") + ":Data:100",
        _("Special Allowance") + ":Data:100",
        _("Dearness Allowance") + ":Data:100",
        _("Conveyance Allowance") + ":Data:100",
        _("Washing Allowance") + ":Data:100",
        _("Total Earnings") + ":Data:100",
        _("D-ESI") + ":Data:100",
        _("D-PF") + ":Data:100",
        _("PT") + ":Data:100",
        _("Advance") + ":Data:100",
        _("Inventory") + ":Data:100",
        _("Client Complaint") + ":Data:100",
        _("Total Deductions") + ":Data:100",
        _("Net Pay") + ":Data:100",

        _("OT Amount") + ":Data:100",
        _("SN PF") + ":Data:100",
        _("SN ESI") + ":Data:100",
        _("SN Net Pay") + ":Data:100",
        _("Overall Net Pay") + ":Data:100",
        
    ]
    return columns

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " from_date= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and to_date = %(to_date)s"
    if filters.get("customer"):
        conditions += " and customer = %(customer)s"
    if filters.get("employee"):
        conditions += " and employee = %(employee)s"
    if filters.get("designation"):
        conditions += " and designation = %(designation)s"

    return conditions, filters

def get_data(filters):
    
        data = []
        conditions, filters = get_conditions(filters)
        sa = frappe.db.sql("""select * from `tabSalary Slips` where %s """%conditions, filters,as_dict=True)
        for i in sa:
            row=[i.employee,
                i.employee_name,
                frappe.db.get_value('Employee',i.employee,'date_of_birth') or "", 
                frappe.db.get_value('Employee',i.employee,'date_of_birth') or "",
                i.company,
                i.department,
                i.from_date,
                i.to_date,
                frappe.db.get_value('Employee',i.employee,'bank_name') or "",
                frappe.db.get_value('Employee',i.employee,'bank_ac_no') or "",
                frappe.db.get_value('Employee',i.employee,'ifsc_code') or "",
                frappe.db.get_value('Employee',i.employee,'bank_branch') or "",
                frappe.db.get_value('Employee',i.employee,'uan_number') or "",
                frappe.db.get_value('Employee',i.employee,'esi_number') or "",
                i.payment_days or 0,
                i.basic or 0,
                i.house_rent_allowance or 0,
                i.special_allowance or 0,
                i.dearness_allowance or 0,
                i.conveyance_allowance or 0,
                i.washing_allowance or 0,
                i.total_earnings or 0,
                i.desi or 0,
                i.dpf or 0,
                i.professional_tax or 0,
                i.advance or 0,
                i.inventory or 0,
                i.client_complaint or 0,
                i.total_deductions or 0,
                i.net_pay or 0 or 0 ,
                i.ot_amount or 0,
                i.sn_pf or 0,
                i.sn_esi or 0,
                i.sn_net_pay or 0,
                i.total_net_pay or 0]
            data.append(row)
        return data

