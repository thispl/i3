# Copyright (c) 2023, Narayanan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

from frappe.utils import date_diff
from frappe.utils import (
    DATE_FORMAT,
    add_to_date,
    getdate,
)
from dateutil.relativedelta import relativedelta

class PayrollProcess(Document):
    @frappe.whitelist()
    def process(self,from_date):
        TEP=0
        nh=''
        cal=0
        
        result = 0  
        SNNET=0
        PT1=0
        EESI = 0  
        h=0
        DPF = 0 
        DESI = 0 
        total1=0
        TEE =0
        HRA=0
        TDP=0
        B=0
        TDE=0
        TE=0
        gross=0
        TD=0
        n=0
        SA=0
        CA=0
        DA=0
        Gross=0
        NetPay=0
        PT=0 
        Days=0
        Advance=0
        TDS=0
        Canteen=0
        Uniform=0
        Rent=0
        OT=0
        Working=0
        OA=0
        WA=0
        Bonus=0
        overtime=0
        TDS=0
        EL=0
        cal=0
        SNPF=''
        Uniform=0
        amt=0
        OD=0
        Advance=0
        Canteen=0
        Rent=0
        SNESI=''
        DESI=''
        DPF =''
        result=''
        EESI=''
        basic=0
        # if frappe.db.exists("Attendance and OT Register",{"customer":self.customer,"start_date":self.start_date,"end_date":self.end_date}):
        # 	mn= frappe.get_all("Attendance and OT Register",{"customer":self.customer,"start_date":self.start_date,"end_date":self.end_date})
        # 	mn = frappe.db.sql("""select * from `tabAttendance and OT Register` where customer = '%s' and start_date = '%s' and end_date = '%s' """%(self.customer,self.start_date,self.end_date),as_dict = True)
        # 	frappe.errprint(mn)
        for p in self.working_employee_details:
                if not frappe.db.exists("Payslip",{"employee":p.employee_code,"designation":p.designation,"customer":self.customer,"from_date":self.start_date,"to_date":self.end_date}):
                    frappe.errprint('naren')
                    form = frappe.new_doc('Payslip')
                    EPF=frappe.db.get_single_value('HR Settings Against Salary', 'epf')
                    EESI=frappe.db.get_single_value('HR Settings Against Salary', 'eesi')
                    DPF=frappe.db.get_single_value('HR Settings Against Salary', 'dpf')
                    DESI=frappe.db.get_single_value('HR Settings Against Salary', 'desi')
                    form.employee = p.employee_code
                    form.employee_name = p.employee_name
                    form.customer = self.customer
                    form.designation=p.designation
                    form.from_date= self.start_date
                    form.designation=p.designation
                    form.to_date= self.end_date
                    form.payment_days= p.total_days
                    form.ot_hours= p.ot_days
                    

                    cus = frappe.get_list("Customer",{'name':self.customer},['*'])
                    for i in cus:
                        val=frappe.get_doc('Customer',i.name)
                        if val.working_day_calculate == 'Type 1 - 26':
                            Working = float(26)
                            frappe.errprint(Working)
                        elif val.working_day_calculate == 'Type 2 - 31':
                            fromdate=self.start_date
                            todate=self.end_date
                            Working=float((date_diff(todate, fromdate))+1)
                            frappe.errprint(Working)
                        if val.ot_calculation == 'Type 1 - 26':
                            cal = float(26)
                            frappe.errprint(cal)
                        elif val.ot_calculation == 'Type 2 - Month Days':
                            fromdate=self.start_date
                            todate=self.end_date
                            cal=float((date_diff(todate, fromdate))+1)
                            frappe.errprint(cal)
                    Days=float(p.total_days) or 0
                    frappe.errprint(Days)
                    for k in val.client_invoice_amount:
                        basic=float(k.basic)
                        hra=float(k.hra)
                        sa=float(k.special_allowance)
                        wa=float(k.washing_allowance)
                        fixed_amount=float(k.fixed_amount)

                        da=float(k.dearness_allowance)
                        total1=basic+hra+sa+wa+da
                        ca=float(k.conveyance_allowance)
                        B   = float((basic/Working)*Days) or 0
                        HRA = float((hra/Working)*Days) or 0.0
                        SA  = float((sa/Working)*Days) or 0.0
                        WA  = float((wa /Working)*Days)or 0.0
                        DA  = float((da /Working)*Days)or 0.0
                        CA  = float((ca/Working)*Days)or 0.0
                        OT  =float ((p.overtime_amount/cal)*Days)or 0
                        OA  = float(p.other_addition)or 0
                        Bonus  =float ((k.bonus/Working)*Days)or 0.0
                        EL  =float ((k.el_wages/Working)*Days)or 0.0
                        OD  = float(p.other_deduction) or 0
                        TDS = float(p.tds) or 0
                        Advance=float(p.advance) or 0
                        Canteen  = float(p.canteen) or 0
                        Uniform  = float(p.uniform) or 0
                        Rent  =float (p.rent) or 0
                        frappe.errprint(B)
                        
                        frappe.errprint(Gross)
                        basic = B
                        hra=HRA
                        special_allowance=SA
                        washing_allowance=WA
                        dearness_allowance=DA
                        conveyance_allowance=CA
                        if k.epf1==1:
                            formula = k.condition_depend_on_salary_component.strip().replace("\n", " ") if k.condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    result = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")

                            
                            if result != '' and float(result) > float(k.fixed_amount):
                                formula = k.amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount}
                                        result = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:
                            formula = k.epf.strip().replace("\n", " ") if k.epf else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    result = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                        if k.eesi1==1:
                            formula = k.condition_depend_on_salary_component.strip().replace("\n", " ") if k.condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance} 
                                    EESI = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            if EESI != '' and float(EESI) > float(k.fixed_amount):
                                formula = k.amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount} or '0'
                                        EESI = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:	
                            formula = k.eesi.strip().replace("\n", " ") if k.eesi else None

                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    EESI = eval(formula, formula_vars)
                                    frappe.errprint(EESI)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")

                        
                        total=0
                        ot=0
                        offot=0
                        tot=0
                        overtime=0
                        ei=float(EESI) or 0.0
                        B_float = float(B) if B else 0.0
                        HRA_float = float(HRA) if HRA else 0.0
                        DA_float = float(DA) if DA else 0.0
                        SA_float = float(SA) if SA else 0.0
                        CA_float = float(CA) if CA else 0.0
                        WA_float = float(WA) if WA else 0.0
                        OT_float = float(OT) if OT else 0.0
                        OD_float = float(OD) if OD else 0.0
                        result_float = float(result) if result else 0.0
                        EESI_float = float(EESI) if EESI else 0.0

                        # Perform the calculation
                        Gross = float(round((B_float + HRA_float + DA_float + SA_float + CA_float + WA_float + OT_float + OD_float + result_float + EESI_float), 2))
                        if(Gross >12500):
                            PT= 208
                        elif(Gross >10000):
                            PT=171
                        elif(Gross > 7500):
                            PT=115
                            frappe.errprint(PT)
                        elif(Gross > 5000):
                            PT=52.5
                        elif(Gross > 3500):
                            PT=22.5
                        else:
                            PT=0
                        frappe.errprint(PT)
                        if k.dpf1==1:
                            formula = k.condition_depend_on_salary_component.strip().replace("\n", " ") if k.condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'gross':gross} 
                                    DPF = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            if DPF != '' and float(DPF) > float(k.fixed_amount):
                                formula = k.amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount} or '0'
                                        DPF = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                            else:	
                                formula = k.dpf.strip().replace("\n", " ") if k.dpf else None

                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                        DPF = eval(formula, formula_vars) 
                                        frappe.errprint(DPF)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:
                            formula = k.dpf.strip().replace("\n", " ") if k.dpf else None

                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    DPF = eval(formula, formula_vars) 
                                    frappe.errprint(DPF)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                        if k.desi1==1:
                            formula = k.condition_depend_on_salary_component.strip().replace("\n", " ") if k.condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance} 
                                    DESI = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            if DESI != '' and float(DESI) > float(k.fixed_amount):
                                formula = k.amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount} or '0'
                                        DESI = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                            else:	
                                formula = k.desi.strip().replace("\n", " ") if k.desi else None

                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,}
                                        DESI = eval(formula, formula_vars)
                                        frappe.errprint(DESI)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:
                            formula = k.desi.strip().replace("\n", " ") if k.desi else None

                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,}
                                    DESI = eval(formula, formula_vars)
                                    frappe.errprint(DESI)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                        for p in self.working_employee_details:
                            if p.employee_code==p.employee_code:
                                offot=p.off_ot_days
                                ot=p.ot_days
                                frappe.errprint(p.ot_days)
                                tot=offot+ot
                        overtime=float(total1/cal*tot)
                        formula = k.sn_pf.strip().replace("\n", " ") if k.sn_pf else None
                        if formula:
                            try:
                                formula_vars = {'over_time':overtime}
                                SNPF = eval(formula, formula_vars) 
                                frappe.errprint(SNPF)
                            except Exception as e:
                                frappe.errprint(f"Error evaluating formula: {str(e)}")
                        else:
                            frappe.errprint("Formula is empty or not provided.")
                        formula = k.sn_esi.strip().replace("\n", " ") if k.sn_esi else None
                        if formula:
                            try:
                                formula_vars = {'over_time':overtime}
                                SNESI = eval(formula, formula_vars) 
                                frappe.errprint(SNESI)
                            except Exception as e:
                                frappe.errprint(f"Error evaluating formula: {str(e)}")
                        else:
                            frappe.errprint("Formula is empty or not provided.")

                    # if (Gross<=20):
                    #     PT=0
                    # elif (Gross>=21000 and Gross<=30000):
                    #     PT=135
                    # elif (Gross>=30001 and Gross<=45000):
                    #     PT=315
                    # elif (Gross>45001 and Gross<=60000):
                    #     PT=690
                    # elif (Gross>60001 and Gross<=75000):
                    #     PT=1025
                    # elif (Gross>75001):
                    #     PT=1250
                
                    # totalval=0
                    # m=0
                    # v=frappe.new_doc("Professional Tax",)
                    # for b in v:
                    #     vt=frappe.get_doc("Professional Tax",b.name)
                    #     for amt in vt.professional_tax_amount:
                    #         nh=(amt.customer)
                    # if nh != self.customer:
                    #     if not frappe.db.exists("Professional Tax", {"employee": p.employee_code,"from_date": ("<=", self.start_date)}):
                    #         pt = frappe.new_doc('Professional Tax')
                    #         ptamt = frappe.get_doc('Payroll Settings','Payroll Settings')
                    #         v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                    #         for b in v:
                    #             vt=frappe.get_doc("Professional Tax",b.name)
                    #             for amt in vt.professional_tax_amount:
                    #                 c=amt.customer
                    #                 t=float(amt.gross_pay)
                    #                 frappe.errprint(t)
                    #                 totalval+=t
                    #                 h=t+Gross
                    #         for pr in ptamt.professional_tax_amount:
                    #             if pr.minimum_amount <=h and pr.maximum_amount>=h :
                    #                 n=amt.pt_amount
                    #                 k=pr.pt_amount-n
                            
                    #         total=0
                        
                        
                    #         pt.employee = p.employee_code
                    #         pt.employee_name = p.employee_name
                    #         total=total+PT
                    #         pt.pt_amount=total or 0
                    #         date_format = "%Y-%m-%d"
                    #         from_date = datetime.strptime(self.start_date, date_format)
                    #         frappe.errprint(from_date)
                    #         if 4 <= from_date.month <= 9:
                    #             from_date = datetime(from_date.year, 4, 1)
                    #         elif 10 <= from_date.month <= 12:
                    #             from_date = datetime(from_date.year + 1, 10, 1)
                    #         else:
                    #             from_date = datetime(from_date.year, 10, 1)
                    #         from_date_str = from_date.strftime(date_format)

                    #         if 4 <= from_date.month <= 9:
                    #             to_date = datetime(from_date.year, 9, 30)
                    #         elif 10 <= from_date.month <= 12:
                    #             to_date = datetime(from_date.year + 1, 3, 31)
                    #         else:
                    #             to_date = datetime(from_date.year, 3, 31)

                    #         to_date_str = to_date.strftime(date_format)
                    #         frappe.errprint(to_date_str)
                    #         pt.from_date = from_date_str
                    #         pt.to_date = to_date_str
                    #         v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                    #         for b in v:
                    #             vt=frappe.get_doc("Professional Tax",b.name)
                    #             for amt in vt.professional_tax_amount:
                    #                 nh=float(amt.pt_amount)
                    #                 op=nh-k
                    #         if op>=0:
                    #             pt.append(
                    #             "professional_tax_amount",
                    #             {
                    #                 "customer": self.customer,
                    #                 "from_date": self.start_date,
                    #                 "to_date": self.end_date,
                    #                 "pt_amount":k,
                    #                 "gross_pay1":Gross,
                    #                 "gross_pay":h   
                                    
                    #             },)
                    #         else:
                    #             k=0
                    #             pt.append(
                    #             "professional_tax_amount",
                    #             {
                    #                 "customer": self.customer,
                    #                 "from_date": self.start_date,
                    #                 "to_date": self.end_date,
                    #                 "gross_pay1":Gross,

                    #                 "pt_amount":k,
                    #                 "gross_pay":h   
                                    
                    #             },)
                    #             m=0
                    #         v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                    #         for b in v:
                    #             vt=frappe.get_doc("Professional Tax",b.name)
                    #             for amt in vt.professional_tax_amount:
                    #                 z=float(amt.pt_amount)
                    #                 v=z+k
                    #                 frappe.errprint(m)
                    #                 pt.pt_amount=v

                        
                    #     pt.save(ignore_permissions=True)
                    TD = float(round((float(DPF) + float(DESI) + float(PT1) + float(Canteen) + float(Rent) + float(Advance) + float(Uniform) + float(TDS)), 2)) or 0
                    frappe.errprint(TD)
                    NetPay=round((Gross-TD),2) or 0
                    frappe.errprint(NetPay)
                    if(self.customer == val.name and p.employee_code==p.employee_code and p.designation==p.designation):
                        form.basic=B
                        form.house_rent_allowance=HRA
                        form.special_allowance=SA
                        form.dearness_allowance=DA
                        form.conveyance_allowance=CA
                        form.washing_allowance=WA
                        form.overtime=OT
                        form.other_addition=OA
                        form.bonus=Bonus
                        form.el_wages=EL

                        form.epf=result
                        form.eesi=EESI
                        form.other_deduction=OD
                        form.dpf=DPF
                        form.desi=DESI
                        form.advance=p.advance
                        form.tds=p.tds
                        form.uniform=p.uniform
                        form.ot_amount = float(overtime)
                        form.ot_amount = float(overtime)
                        form.sn_pf = float(SNPF) if SNPF else 0.0
                        form.sn_esi = float(SNESI) if SNESI else 0.0

                        form.net_pay1 =form.ot_amount-form.sn_pf - form.sn_esi 
                        form.canteen=p.canteen
                        form.rent=p.rent
                        form.total_earnings = Gross
                        form.total_deductions= TD
                        form.net_pay=NetPay
                        form.working_days=Working
                        form.duty_days=p.duty_days
                        
                        form.professional_tax=PT
                        form.total_net_pay=form.net_pay+form.net_pay1
            
                    form.save(ignore_permissions=True)
                    frappe.db.commit()

                else:
                    
                    frappe.errprint("HIiiiiiiiiiiiiiii")
                    form = frappe.get_doc("Payslip",{"employee":p.employee_code,"designation":p.designation,"customer":self.customer,"from_date":self.start_date,"to_date":self.end_date})
                    EPF=frappe.db.get_single_value('HR Settings Against Salary', 'epf')
                    EESI=frappe.db.get_single_value('HR Settings Against Salary', 'eesi')
                    DPF=frappe.db.get_single_value('HR Settings Against Salary', 'dpf')
                    DESI=frappe.db.get_single_value('HR Settings Against Salary', 'desi')
                    form.employee = p.employee_code
                    form.employee_name = p.employee_name
                    form.customer = self.customer
                    form.from_date= self.start_date
                    form.designation=p.designation
                    form.to_date= self.end_date
                    form.payment_days= p.total_days
                    form.ot_hours= p.ot_days+p.off_ot_days
                    

                    cus = frappe.get_list("Customer",{'name':self.customer},['*'])
                    for i in cus:
                        val=frappe.get_doc('Customer',i.name)
                        if val.working_day_calculate == 'Type 1 - 26':
                            Working = float(26)
                            frappe.errprint(Working)
                        elif val.working_day_calculate == 'Type 2 - 31':
                            fromdate=self.start_date
                            todate=self.end_date
                            Working=float((date_diff(todate, fromdate))+1)
                            frappe.errprint(Working)
                        if val.ot_calculation == 'Type 1 - 26':
                            cal = float(26)
                            frappe.errprint(cal)
                        elif val.ot_calculation == 'Type 2 - Month Days':
                            fromdate=self.start_date
                            todate=self.end_date
                            cal=float((date_diff(todate, fromdate))+1)
                            frappe.errprint(cal)
                        if p.employee_code==p.employee_code:
                            duty=p.duty_days

                    Days=float(p.total_days) or 0
                    frappe.errprint(Days)
                    for k in val.client_invoice_amount:
                        basic=float(k.basic)
                        hra=float(k.hra)
                        sa=float(k.special_allowance)
                        wa=float(k.washing_allowance)
                        fixed_amount=float(k.fixed_amount)

                        da=float(k.dearness_allowance)
                        ca=float(k.conveyance_allowance)
                        total1=basic+hra+sa+wa+da+ca
                        B   = float((basic/Working)*Days) or 0
                        HRA = float((hra/Working)*Days) or 0.0
                        SA  = float((sa/Working)*Days) or 0.0
                        WA  = float((wa /Working)*Days)or 0.0
                        DA  = float((da /Working)*Days)or 0.0
                        CA  =float ((ca/Working)*Days)or 0.0
                        Bonus  =float ((k.bonus/Working)*Days)or 0.0
                        EL  =float ((k.el_wages/Working)*duty)or 0.0
                        OT  = float((p.overtime_amount/cal)*Days)or 0
                        OA  =float (p.other_addition)or 0
                        OD  = float(p.other_deduction) or 0
                        TDS = float(p.tds) or 0
                        Advance=(p.advance) or 0
                        Canteen  = (p.canteen) or 0
                        Uniform  = (p.uniform) or 0
                        Rent  = (p.rent) or 0
                        frappe.errprint(B)
                        
                        frappe.errprint(Gross)
                        basic = B
                        bonus=Bonus
                        hra=HRA
                        special_allowance=SA
                        washing_allowance=WA
                        dearness_allowance=DA
                        conveyance_allowance=CA
                        if k.epf1==1:
                            formula = k.condition_depend_on_salary_component.strip().replace("\n", " ") if k.condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    result = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")

                            
                            if result != '' and float(result) > float(k.fixed_amount):
                                formula = k.amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount}
                                        result = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:
                            formula = k.epf.strip().replace("\n", " ") if k.epf else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    result = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                        if k.eesi1==1:
                            formula = k.condition_depend_on_salary_component.strip().replace("\n", " ") if k.condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance} 
                                    EESI = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            if EESI != '' and float(EESI) > float(k.fixed_amount):
                                formula = k.amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount} or '0'
                                        EESI = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:	
                            formula = k.eesi.strip().replace("\n", " ") if k.eesi else None

                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    EESI = eval(formula, formula_vars)
                                    frappe.errprint(EESI)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")


                        
                        
                        total=0
                        ot=0
                        offot=0
                        tot=0
                        overtime=0
                        B_float = float(B) if B else 0.0
                        HRA_float = float(HRA) if HRA else 0.0
                        DA_float = float(DA) if DA else 0.0
                        SA_float = float(SA) if SA else 0.0
                        CA_float = float(CA) if CA else 0.0
                        WA_float = float(WA) if WA else 0.0
                        OT_float = float(OT) if OT else 0.0
                        OD_float = float(OD) if OD else 0.0
                        Bonus=float(Bonus) if Bonus else 0.0
                        El=float(EL) if EL else 0.0

                        result_float = float(result) if result else 0.0
                        EESI_float = float(EESI) if EESI else 0.0
                        Gross = float(round((B_float + HRA_float + DA_float + SA_float + CA_float + WA_float + Bonus+EL+ OT_float + OD_float + result_float + EESI_float), 2))
                        gross=Gross
                        frappe.errprint(gross)
                        frappe.errprint('naren')

                        if(Gross >12500):
                            PT= 208
                        elif(Gross >10000):
                            PT=171
                        elif(Gross > 7500):
                            PT=115
                            frappe.errprint(PT)
                        elif(Gross > 5000):
                            PT=52.5
                        elif(Gross > 3500):
                            PT=22.5
                        else:
                            PT=0
                        if k.dpf1==True:
                            frappe.errprint('naren')
                            formula = k.dpf_condition_depend_on_salary_component.strip().replace("\n", " ") if k.dpf_condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'gross':gross} 
                                    DPF = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                    frappe.errprint(DPF)
                                    frappe.errprint('naren')
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            if DPF != '' and float(DPF) > float(k.dpf_fixed_amount):
                                formula = k.dpf_amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.dpf_amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount} or '0'
                                        DPF = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                        frappe.errprint(DPF)
                                        frappe.errprint('naren')
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                            
                            else:	
                                formula = k.dpf.strip().replace("\n", " ") if k.dpf else None

                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                        DPF = eval(formula, formula_vars) 
                                        frappe.errprint(DPF)
                                        frappe.errprint(DPF)
                                        frappe.errprint('naren')
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:
                            formula = k.dpf.strip().replace("\n", " ") if k.dpf else None

                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance}
                                    DPF = eval(formula, formula_vars) 
                                    frappe.errprint(DPF)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            
                        if k.desi1==True:
                            formula = k.desi_condition_depend_on_salary_component.strip().replace("\n", " ") if k.desi_condition_depend_on_salary_component else None
                            frappe.errprint(formula)
                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance} 
                                    DESI = eval(formula, formula_vars)
                                    frappe.errprint(result)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                            if DESI != '' and float(DESI) > float(k.desi_fixed_amount):
                                formula = k.desi_amount_greater_than_fixed_amount.strip().replace("\n", " ") if k.desi_amount_greater_than_fixed_amount else None
                                frappe.errprint(formula)
                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,'fixed_amount':fixed_amount} or '0'
                                        DESI = eval(formula, formula_vars)
                                        frappe.errprint(result)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                            else:	
                                formula = k.desi.strip().replace("\n", " ") if k.desi else None

                                if formula:
                                    try:
                                        formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,}
                                        DESI = eval(formula, formula_vars)
                                        frappe.errprint(DESI)
                                    except Exception as e:
                                        frappe.errprint(f"Error evaluating formula: {str(e)}")
                                else:
                                    frappe.errprint("Formula is empty or not provided.")
                        else:	
                            formula = k.desi.strip().replace("\n", " ") if k.desi else None

                            if formula:
                                try:
                                    formula_vars = {'basic': basic, 'hra': hra,'special_allowance':special_allowance,'gross':gross,'bonus':bonus,'dearness_allowance':dearness_allowance,'conveyance_allowance':conveyance_allowance,'washing_allowance':washing_allowance,}
                                    DESI = eval(formula, formula_vars)
                                    frappe.errprint(DESI)
                                except Exception as e:
                                    frappe.errprint(f"Error evaluating formula: {str(e)}")
                            else:
                                frappe.errprint("Formula is empty or not provided.")
                        
                        for p in self.working_employee_details:
                            if p.employee_code == p.employee_code:
                                offot=p.off_ot_days
                                ot=p.ot_days
                                tot=form.ot_hours
                            frappe.errprint(tot)
                            frappe.errprint(cal)
                            frappe.errprint(total1)
                            frappe.errprint('hiiii')
                            overtime=float(total1 / cal * tot)
                            frappe.errprint(overtime)
                        formula = k.sn_pf.strip().replace("\n", " ") if k.sn_pf else None
                        if formula:
                            try:
                                formula_vars = {'over_time':overtime}
                                SNPF = eval(formula, formula_vars) 
                                frappe.errprint(SNPF)
                            except Exception as e:
                                frappe.errprint(f"Error evaluating formula: {str(e)}")
                        else:
                            frappe.errprint("Formula is empty or not provided.")
                        formula = k.sn_esi.strip().replace("\n", " ") if k.sn_esi else None
                        if formula:
                            try:
                                formula_vars = {'over_time':overtime}
                                SNESI = eval(formula, formula_vars) 
                                frappe.errprint(SNESI)
                            except Exception as e:
                                frappe.errprint(f"Error evaluating formula: {str(e)}")
                        else:
                            frappe.errprint("Formula is empty or not provided.")

                        # if (Gross<=20):
                        #     PT=0
                        # elif (Gross>=21000 and Gross<=30000):
                        #     PT=135
                        # elif (Gross>=30001 and Gross<=45000):
                        #     PT=315
                        # elif (Gross>45001 and Gross<=60000):
                        #     PT=690
                        # elif (Gross>60001 and Gross<=75000):
                        #     PT=1025
                        # elif (Gross>75001):
                        #     PT=1250
                    
                        totalval=0
                        m=0
                        # v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                        # for b in v:
                        #     vt=frappe.get_doc("Professional Tax",b.name)
                        #     for amt in vt.professional_tax_amount:
                        #         nh=(amt.customer)
                        # if nh != self.customer:
                        #     if frappe.db.exists("Professional Tax", {"employee": p.employee_code,"from_date": ("<=", self.start_date)}):
                        #         pt = frappe.get_doc('Professional Tax',{'employee':p.employee_code})
                        #         ptamt = frappe.get_doc('Payroll Settings','Payroll Settings')
                        #         v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                        #         for b in v:
                        #             vt=frappe.get_doc("Professional Tax",b.name)
                        #             for amt in vt.professional_tax_amount:
                        #                 c=amt.customer
                        #                 t=float(amt.gross_pay)
                        #                 frappe.errprint(t)
                        #                 totalval+=t
                        #                 h=t+Gross
                        #         for pr in ptamt.professional_tax_amount:
                        #             if pr.minimum_amount <=h and pr.maximum_amount>=h :
                        #                 n=float(amt.pt_amount)
                        #                 k=pr.pt_amount-n
                                
                        #         total=0
                            
                            
                        #         pt.employee = p.employee_code
                        #         pt.employee_name = p.employee_name
                        #         total=total+PT
                        #         pt.pt_amount=total or 0
                        #         date_format = "%Y-%m-%d"
                        #         from_date = datetime.strptime(self.start_date, date_format)
                        #         frappe.errprint(from_date)
                        #         if 4 <= from_date.month <= 9:
                        #             from_date = datetime(from_date.year, 4, 1)
                        #         elif 10 <= from_date.month <= 12:
                        #             from_date = datetime(from_date.year + 1, 10, 1)
                        #         else:
                        #             from_date = datetime(from_date.year, 10, 1)
                        #         from_date_str = from_date.strftime(date_format)

                        #         if 4 <= from_date.month <= 9:
                        #             to_date = datetime(from_date.year, 9, 30)
                        #         elif 10 <= from_date.month <= 12:
                        #             to_date = datetime(from_date.year + 1, 3, 31)
                        #         else:
                        #             to_date = datetime(from_date.year, 3, 31)

                        #         to_date_str = to_date.strftime(date_format)
                        #         frappe.errprint(to_date_str)
                        #         pt.from_date = from_date_str
                        #         pt.to_date = to_date_str
                        #         v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                        #         for b in v:
                        #             vt=frappe.get_doc("Professional Tax",b.name)
                        #             for amt in vt.professional_tax_amount:
                        #                 nh=float(amt.pt_amount)
                        #                 op=nh-k
                        #         if op>=0:
                        #             pt.append(
                        #             "professional_tax_amount",
                        #             {
                        #                 "customer": self.customer,
                        #                 "from_date": self.start_date,
                        #                 "to_date": self.end_date,
                        #                 "pt_amount":k,
                        #                 "gross_pay1":Gross,
                        #                 "gross_pay":h   
                                        
                        #             },)
                        #         else:
                        #             k=0
                        #             pt.append(
                        #             "professional_tax_amount",
                        #             {
                        #                 "customer": self.customer,
                        #                 "from_date": self.start_date,
                        #                 "to_date": self.end_date,
                        #                 "gross_pay1":Gross,

                        #                 "pt_amount":k,
                        #                 "gross_pay":h   
                                        
                        #             },)
                        #             m=0
                        #         v=frappe.get_all("Professional Tax",{'employee':p.employee_code},['*'])
                        #         for b in v:
                        #             vt=frappe.get_doc("Professional Tax",b.name)
                        #             for amt in vt.professional_tax_amount:
                        #                 z=float(amt.pt_amount)
                        #                 v=z+k
                        #                 frappe.errprint(m)
                        #                 pt.pt_amount=v

                            
                        #     pt.save(ignore_permissions=True)
                        TD = float(round((float(DPF) + float(DESI) + float(PT) + float(Canteen) + float(Rent) + float(Advance) + float(Uniform) + float(TDS)), 2)) or 0
                        frappe.errprint(TD)
                        NetPay=round((Gross-TD),2) or 0
                        frappe.errprint(NetPay)
                        if(self.customer == val.name and p.employee_code == p.employee_code and k.designation == p.designation):
                            form.basic=B
                            form.house_rent_allowance=HRA
                            form.special_allowance=SA
                            form.dearness_allowance=DA
                            form.conveyance_allowance=CA
                            form.washing_allowance=WA
                            form.overtime=OT
                            form.other_addition=OA
                            form.bonus=Bonus
                            form.el_wages=EL

                            form.epf=result
                            form.eesi=EESI
                            form.other_deduction=OD
                            form.dpf=DPF
                            form.desi=DESI
                            form.advance=p.advance
                            form.tds=p.tds
                            form.uniform=p.uniform
                            form.ot_amount = float(overtime)
                            form.sn_pf = float(SNPF) if SNPF else 0.0
                            form.sn_esi = float(SNESI) if SNESI else 0.0

                            form.net_pay1 =form.ot_amount - form.sn_pf - form.sn_esi 
                            form.canteen=float(Canteen) 
                            form.rent=p.rent
                            form.total_earnings = Gross
                            form.total_deductions= TD
                            form.net_pay=NetPay
                            form.working_days=Working
                            form.duty_days=p.duty_days
                            form.professional_tax=PT
                            form.total_net_pay=form.net_pay+form.net_pay1
                
                    form.save(ignore_permissions=True)
                    frappe.db.commit()


@frappe.whitelist()
def get_end_date(start_date, frequency):
    start_date = getdate(start_date)
    frequency = frequency.lower() if frequency else "monthly"
    kwargs = (
        get_frequency_kwargs(frequency) if frequency != "bimonthly" else get_frequency_kwargs("monthly")
    )
    end_date = add_to_date(start_date, **kwargs) - relativedelta(days=1)
    if frequency == "monthly":
        return dict(end_date=end_date.strftime(DATE_FORMAT))

    else:
        return dict(end_date="")

def get_frequency_kwargs(frequency_name):
    frequency_dict = {
        "monthly": {"months": 1},
        "fortnightly": {"days": 14},
        "weekly": {"days": 7},
        "daily": {"days": 1},
    }
    return frequency_dict.get(frequency_name)