# # import frappe
# # from frappe import _

# # def execute(filters=None):
# # 	columns=get_columns(filters)
# # 	data = get_data(filters)
# # 	return columns, data

# # def get_columns(filters):
# # 	columns=[]
# # 	columns += [
# # 		_("Employee") + ":Link/Employee:110",
# # 		_("Employee Name") + ":Data:100",

# # 	]
# # 	return columns

# # def get_conditions(filters):
# # 	conditions = ""
# # 	if filters.get("from_date"):
# # 		conditions += " from_date= %(from_date)s"
# # 	if filters.get("to_date"):
# # 		conditions += " and to_date = %(to_date)s"
# # 	return conditions, filters

# # def get_data(filters):
# # 	data = []
# # 	conditions, filters = get_conditions(filters)
# # 	sa = frappe.db.sql("""select * from `tabSalary Slips` where  from_date BETWEEN %s and %s """(from_date,to_date),as_dict=True)

# # 	for slip in sa:
# # 		frappe.errprint(slip)
# # 		row = [slip.employee,slip.employee_name]
# # 		# row = [slip['employee'],slip['employee_name']]
# # 		data.append(row)

# # 	return data

# import frappe
# from frappe import _

# def execute(filters=None):
#     columns = get_columns(filters)
#     data = get_data(filters)
#     return columns, data

# def get_columns(filters):
#     columns = []
#     columns += [
#         _("Employee") + ":Link/Employee:110",
#         _("Employee Name") + ":Data:100",
# 		_("From Date") + ":Data:110",
# 		_("To Date") + ":Data:100",
# 		_("Professional Tax") + ":Data:100",
#     ]  
#     return columns

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("from_date"):
#         conditions += " from_date >= %(from_date)s"
#     if filters.get("to_date"):
#         if conditions:
#             conditions += " and "
#         conditions += "to_date <= %(to_date)s"
#     return conditions, filters

# def get_data(filters):
#     employee=''
#     data = []
#     conditions, filters = get_conditions(filters)
    
#     # Define the from_date and to_date variables
#     from_date = filters.get("from_date")
#     to_date = filters.get("to_date")

#     sa = frappe.db.sql(
#         """
#         select * from `tabPayslip`
#         where from_date BETWEEN %(from_date)s and %(to_date)s
#         """,
#         {"from_date": from_date, "to_date": to_date},
#         as_dict=True
#     )

#     for slip in sa:
#         frappe.errprint(slip)
#         if(slip.employee == slip.employee):
#             row = [
#             employee+=slip.employee, 
#             slip.employee_name,
#             filters.from_date,
#             filters.to_date,
#             slip.professional_tax
#             ]
#             data.append(row)

#     return data

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        _("Employee") + ":Link/Employee:110",
        _("Employee Name") + ":Data:100",
        _("From Date") + ":Date:110",
        _("To Date") + ":Date:100",
        _("Professional Tax") + ":Currency:100",
    ]
    return columns

def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append("from_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("to_date <= %(to_date)s")
    if filters.get("employee"):
        conditions.append("employee = %(employee)s")
    return " and ".join(conditions), filters
    
def get_data(filters):
    data = []
    conditions, filters = get_conditions(filters)

    # Define the from_date and to_date variables
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    sa = frappe.db.sql(
        """
        select employee, employee_name, from_date, to_date, professional_tax
        from `tabPayslip`
        where from_date BETWEEN %(from_date)s and %(to_date)s
        """,
        {"from_date": from_date, "to_date": to_date},
        as_dict=True
    )

    employee_accumulator = {}
    for slip in sa:
        employee_id = slip.employee
        if employee_id not in employee_accumulator:
            employee_accumulator[employee_id] = {
                "employee_name": slip.employee_name,
                "from_date": filters.from_date,
                "to_date": filters.to_date,
                "professional_tax": 0,
            }
        employee_accumulator[employee_id]["professional_tax"] += slip.professional_tax

    for employee_id, employee_data in employee_accumulator.items():
        data.append([
            employee_id,
            employee_data["employee_name"],
            employee_data["from_date"],
            employee_data["to_date"],
            employee_data["professional_tax"]
        ])

    return data