# Copyright (c) 2023, Narayanan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
import erpnext
from frappe.utils.data import add_days, today
from frappe.utils import  formatdate
from frappe.utils import format_datetime

def execute(filters=None):
	if not filters:
		filters = {}
	currency = None
	if filters.get("currency"):
		currency = filters.get("currency")
	company_currency = erpnext.get_company_currency(filters.get("company"))
	salary_slips = get_salary_slips(filters, company_currency)
	if not salary_slips:
		return [], []

	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
	ss_ded_map = get_ss_ded_map(salary_slips, currency, company_currency)
	doj_map = get_employee_doj_map()
	

	data = []
	for ss in salary_slips:
		sum_emp = frappe.db.sql("""select sum(basic + house_rent_allowance + dearness_allowance + unit_allowance ) as total from `tabEmployee` where employee='%s' """%(ss.employee),as_dict=1)[0]
		row = [
				ss.employee,
				ss.employee_name,
				frappe.db.get_value('Employee',ss.employee,'contractor') or "",
				frappe.db.get_value('Employee',ss.employee,'rank') or "",
				frappe.db.get_value('Employee',ss.employee,'designation') or "",
				formatdate(frappe.db.get_value('Employee',ss.employee,'date_of_birth') or ""),
				formatdate(frappe.db.get_value('Employee',ss.employee,'date_of_joining') or ""),
				frappe.db.get_value('Employee',ss.employee,'uan_number') or "-",
				frappe.db.get_value('Employee',ss.employee,'esi_number') or "-",
				frappe.db.get_value('Employee',ss.employee,'duty_days') or 0,
				frappe.db.get_value('Employee',ss.employee,'week_off') or 0,
				ss.payment_days,
				
				frappe.db.get_value('Employee',ss.employee,'basic') or 0,
				frappe.db.get_value('Employee',ss.employee,'dearness_allowance') or 0,
				frappe.db.get_value('Employee',ss.employee,'house_rent_allowance') or 0,
				frappe.db.get_value('Employee',ss.employee,'unit_allowance') or 0,
				sum_emp['total'] or 0,
				int(frappe.get_value('Salary Detail',{'salary_component':"Basic",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Dearness Allowance",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"House Rent Allowance",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Unit Allowance",'parent':ss.name},["amount"]) or 0),
				ss.gross_pay,
				int(frappe.get_value('Salary Detail',{'salary_component':"Employee State Insurance",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Canteen",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Uniform",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"L/w Fund",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Personal Accident Insurance",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Advance",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Other Deduction",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Attrti",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Insurance",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"ID Card",'parent':ss.name},["amount"]) or 0),
					int(frappe.get_value('Salary Detail',{'salary_component':"NAPL",'parent':ss.name},["amount"]) or 0),
				int(frappe.get_value('Salary Detail',{'salary_component':"Professional Tax",'parent':ss.name},["amount"]) or 0),
				ss.total_deduction or 0,
				ss.net_pay or 0
            ]
		    	
		frappe.errprint(int(frappe.get_value('Salary Detail',{'abbr':"ESI",'parent':ss.name},["amount"]) or 0))
		data.append(row)
		frappe.errprint(row)

		if ss.branch is not None:
			columns[3] = columns[3].replace("-1", "120")
		if ss.department is not None:
			columns[4] = columns[4].replace("-1", "120")
		if ss.designation is not None:
			columns[5] = columns[5].replace("-1", "120")
		if ss.leave_without_pay is not None:
			columns[9] = columns[9].replace("-1", "130")

	return columns, data

def get_columns(salary_slips):
	columns = [
		_("Employee NO") + ":Employee:120",
		_("Employee Name") + "::200",
		_("Contractor") + "::100",
		_("Rank") + "::100",
		_("Designation") + "::100",
		# _("Father's / Spouse's Name") + "::200",
		# _("Relationship") + "::100",
		_("Date of Birth") + "::120",
		# _("Department") + "::100",
		# _("Designation") + "::100",
		# _("Principal Employer") + "::100",
		# _("Unit") + "::60",
		# _("Invoice Name") + "::200",
		_("Date of Joining") + "::120",
		_("UAN Number") + "::100",
		_("ESI Number") + "::100",
		# _("Bank A/c Number") + "::120",
		# _("Bank Name") + "::120",
		_("Duty Days") + "::120",
		_("Week Off") + "::120",
		_("No.Of Days ") + "::120",
		_("Fixed Basic") + ":Data:100",
		_("Fixed Dearness Allowance") + ":Data:200",
		_("Fixed House Rent Allowance") + ":Data:200",
		_("Fixed Unit Allowance") + ":Data:200",
		# _("Fixed Conveyance Allowance") + ":Data:200",
		# _("Fixed Medical Allowance") + ":Data:200",
		# _("Fixed Special Allowance") + ":Data:200",
		# _("Fixed Other Allowance") + ":Data:200",
		_("Fixed Total") + ":Data:150",
		_("Earned Basic") + ":Data:100",
		_("Earned Dearness Allowance") + ":Data:200",
		_("Earned House Rent Allowance") + ":Data:200",
		_("Earned Unit Allowance") + ":Data:200",
		# _("Earned Conveyance Allowance") + ":Data:200",
		# _("Earned Medical Allowance") + ":Data:200",
		# _("Earned Special Allowance") + ":Data:200",
		# _("Earned Other Allowance") + ":Data:200",
		# # _("Lunch Allowance") + ":Data:150",
		# _("OT Hours") + ":Data:120",
		# _("OT Amount") + ":Data:120",
		_("Gross Pay") + ":Currency:150",
		
		_("Deduction Employee State Insurence") + ":Data:150",
		_("Deduction Provident Fund") + ":Data:150",
		_("Deduction Canteen") + ":Data:150",
		_("Deduction Uniform") + ":Data:150",
		_("Deduction L/w Fund") + ":Data:150",
		_("Deduction Personal Accident Insurance") + ":Data:150",
		_("Deduction Advance") + ":Data:150",
		_("Other Deduction") + ":Data:150",
		_("Deduction Attrti") + ":Data:150",
		_("Deduction Insurance") + ":Data:150",
		_("Deduction ID Card") + ":Data:150",
		_("Deduction NAPL") + ":Data:150",
		_("Deduction Professional Tax") + ":Data:150",
		# _("Leave Encashment") + ":Data:150",
		# _("Service Charges") + ":Data:150",
		# _("Total payable to MVL") + ":Data:150",
		# _("Provident Fund") + ":Data:150",
		# _("Employee State Insurence") + ":Data:150",
		
		# _("Salary Advance Detection") + ":Data:150",
		
		_("Total Deductions") + ":Data:150",
		_("Net Pay") + ":Data:150"
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql(
		"""select distinct sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)"""
		% (", ".join(["%s"] * len(salary_slips))),
		tuple([d.name for d in salary_slips]),
		as_dict=1,
	):
		salary_components[_(component.type)].append(component.salary_component)

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters, company_currency):
	filters.update({"from_date": filters.get("from_date"), 
	"to_date": filters.get("to_date"),
	"contractor":filters.get("contractor")
	})
	conditions, filters = get_conditions(filters, company_currency)
	salary_slips = frappe.db.sql(
		"""select * from `tabSalary Slip` where docstatus != 2 and %s order by employee"""% conditions,
		filters,
		as_dict=1,
	)
	return salary_slips or []


def get_conditions(filters, company_currency):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}
	if filters.get("docstatus"):
		conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])
	if filters.get("from_date"):
		conditions += " and start_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " and end_date <= %(to_date)s"
	if filters.get("company"):
		conditions += " and company = %(company)s"
	if filters.get("contractor"):
		conditions += " and contractor = %(contractor)s"
	if filters.get("currency") and filters.get("currency") != company_currency:
		conditions += " and currency = %(currency)s"
	return conditions, filters

def get_employee_doj_map():
	return frappe._dict(frappe.db.sql("""SELECT employee,date_of_joining FROM `tabEmployee` """))

def get_ss_earning_map(salary_slips, currency, company_currency):
	ss_earnings = frappe.db.sql(
		"""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)"""
		% (", ".join(["%s"] * len(salary_slips))),
		tuple([d.name for d in salary_slips]),
		as_dict=1,
	)
	
	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_earning_map[d.parent][d.salary_component] += flt(d.amount) * flt(
				d.exchange_rate if d.exchange_rate else 1
			)
		else:
			ss_earning_map[d.parent][d.salary_component] += flt(d.amount)
	return ss_earning_map


def get_ss_ded_map(salary_slips, currency, company_currency):
	ss_deductions = frappe.db.sql(
		"""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)"""
		% (", ".join(["%s"] * len(salary_slips))),
		tuple([d.name for d in salary_slips]),
		as_dict=1,
	)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_ded_map[d.parent][d.salary_component] += flt(d.amount) * flt(
				d.exchange_rate if d.exchange_rate else 1
			)
		else:
			ss_ded_map[d.parent][d.salary_component] += flt(d.amount)
	return ss_ded_map
