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

class AttendanceBonus(Document):
    @frappe.whitelist()
    def date(self):
        Days = float((date_diff(to_date, from_date)) + 1)
        self.total_days = Days
        frappe.errprint( self.total_days)

    @frappe.whitelist()
    def percent(self):
        if self.actual_amount_baed_on_percentage==1:
            self.actual_amount=self.amount_based_on_percentage

    @frappe.whitelist()
    def amounts(self):
        if self.actual_amount_based_on_amount==1:
            self.actual_amount=self.amount or 0

# @frappe.whitelist()
# def get_date(fromdate,todate):
#         Days = float((date_diff(todate, fromdate)) + 1)
#         return Days

@frappe.whitelist()
def get_val():
        DESI=frappe.db.get_single_value('HR Settings Against Salary', 'bonus_process')
        return DESI

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

@frappe.whitelist()
def get_end_date(start_date, frequency):
        start_date = getdate(start_date)
        frequency = frequency.lower() if frequency else "yearly"  
        kwarg = get_frequency_kwargs(frequency)
        end_date = add_to_date(start_date, **kwarg) - relativedelta(days=1)
        return dict(end_date=end_date.strftime(DATE_FORMAT))
        
def get_frequency_kwargs(frequency_name):
    frequency_dict = {
        "yearly": {"years": 1},  # Adjusted for yearly frequency
        "monthly": {"months": 1},
        "fortnightly": {"days": 14},
        "weekly": {"days": 7},
        "daily": {"days": 1},
    }
    return frequency_dict.get(frequency_name, {})
              