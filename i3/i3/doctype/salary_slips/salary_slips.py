# Copyright (c) 2023, Narayanan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from frappe.utils import (
	DATE_FORMAT,
	add_to_date,
	getdate,
)
from dateutil.relativedelta import relativedelta

class SalarySlips(Document):
	@frappe.whitelist()
	def process(self):
		Basic=0
		HRA=0
		SA=0
		WA=0
		CA=0
		TEP=0
		EPF = 0  
		DA=0
		OT=0
		OA=0
		EESI = 0  
		DPF = 0 
		DESI = 0 
		TEE =0
		TDP=0
		OD=0
		TDE=0
		TE=0
		TD=0
		Net=0
		PT=0 
		Deduction=0
		SNESI=0
		Advance=0
		TDS=0
		Canteen=0
		Uniform=0
		Rent=0
		Total=0
		Payment=0
		SNPF=0
		OTDays=0
		SNNET=0
		OT_amt=0
		cus = frappe.db.sql("""select * from `tabPayslip`""",as_dict=True)
		for slip in cus:
			if slip.get('employee') == self.employee :
				frappe.errprint(slip.get('name'))
				Payment += int(slip.get('payment_days')) or 0
				OTDays += int(slip.get('ot_hours')) or 0
				Basic += slip.get('basic') or 0
				HRA += slip.get('house_rent_allowance') or 0
				SA += slip.get('special_allowance') or 0
				DA += slip.get('dearness_allowance') or 0
				CA += slip.get('conveyance_allowance') or 0
				WA += slip.get('washing_allowance') or 0
				OT += slip.get('overtime') or 0
				OA += slip.get('other_addition') or 0
				EPF += slip.get('epf') or 0
				EESI += slip.get('eesi') or 0
				Deduction += slip.get('deductions') or 0
				OD += slip.get('other_deduction') or 0
				DPF += slip.get('dpf') or 0
				DESI += slip.get('desi') or 0
				PT += slip.get('professional_tax') or 0
				Advance += slip.get('advance') or 0
				TDS += slip.get('tds') or 0
				Canteen += slip.get('canteen') or 0
				Uniform += slip.get('uniform') or 0
				Rent += slip.get('rent') or 0
				TE += slip.get('total_earnings') or 0
				Net += slip.get('net_pay') or 0
				TD += slip.get('total_deductions') or 0
				OT_amt+=slip.get('ot_amount') or 0
				SNPF+=slip.get('sn_pf') or 0
				SNESI+=slip.get('sn_esi') or 0
				Total+=slip.get('total_net_pay') or 0
				SNNET+=slip.get('net_pay1') or 0

			self.from_date=slip.get('from_date')
			self.to_date=slip.get('to_date')
			self.working_days=slip.get('working_days')
			self.designation=slip.get('designation')
		self.payment_days=Payment
		self.ot_hours=OTDays
		self.basic=Basic
		self.house_rent_allowance=HRA
		self.special_allowance=SA
		self.dearness_allowance=DA
		self.conveyance_allowance=CA
		self.washing_allowance=WA
		self.overtime=OT
		self.other_addition=OA
		self.epf=EPF
		self.eesi=EESI
		self.deductions=Deduction
		self.other_deduction=OD
		self.dpf=DPF
		self.desi=DESI
		self.professional_tax=PT
		self.advance=Advance
		self.tds=TDS
		self.canteen=Canteen
		self.uniform=Uniform
		self.rent=Rent
		self.total_earnings=TE
		self.net_pay=Net
		self.total_deductions=TD
		self.ot_amount=OT_amt
		self.sn_pf=SNPF
		self.sn_esi=SNESI
		self.total_net_pay=Total
		self.sn_net_pay=SNNET

# @frappe.whitelist()
# def get_end_date(start_date, frequency):
# 	start_date = getdate(start_date)
# 	frequency = frequency.lower() if frequency else "monthly"
# 	kwargs = (
# 		get_frequency_kwargs(frequency) if frequency != "bimonthly" else get_frequency_kwargs("monthly")
# 	)
# 	end_date = add_to_date(start_date, **kwargs) - relativedelta(days=1)
# 	if frequency == "monthly":
# 		return dict(end_date=end_date.strftime(DATE_FORMAT))

# 	else:
# 		return dict(end_date="")

# def get_frequency_kwargs(frequency_name):
# 	frequency_dict = {
# 		"monthly": {"months": 1},
# 		"fortnightly": {"days": 14},
# 		"weekly": {"days": 7},
# 		"daily": {"days": 1},
# 	}
# 	return frequency_dict.get(frequency_name)