import os,json
import frappe
from frappe import _
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.utils import now_datetime, formatdate,random_string
# from frappe.translate import print_language
from frappe.utils.pdf import get_pdf
from frappe.utils.background_jobs import enqueue
from PyPDF2 import PdfFileWriter



no_cache = 1

base_template_path = "www/printview.html"
standard_format = "templates/print_formats/standard.html"

from frappe.www.printview import validate_print_permission

@frappe.whitelist()
def enqueue_download_multi_pdf(start_date, end_date, customer=None, employee=None):
    conditions = ''
    if customer:
        conditions += f' and customer="{customer}"'
    if employee:
        conditions += f' and employee="{employee}"'

    payslip_data = frappe.db.sql(
        f"SELECT name FROM `tabPayslip` WHERE from_date = '{start_date}' AND to_date = '{end_date}' {conditions}",
        as_dict=True
    )
    
    payslip_names = [row['name'] for row in payslip_data]
    
    enqueue(
        download_multi_pdf,
        queue='default',
        timeout=8000,
        event='download_multi_pdf',
        doctype="Payslip",
        name=json.dumps(payslip_names),
        format='Salary Slip'
    )
    
    frappe.msgprint("Payslip Download is successfully initiated. Kindly wait for some time and refresh the page.")  
def download_multi_pdf(doctype, name, format=None, no_letterhead=False, letterhead=None, options=None):
    import json

    output = PdfFileWriter()

    if isinstance(options, str):
        options = json.loads(options)

    if not isinstance(doctype, dict):
        result = json.loads(name)

        # Concatenating pdf files
        for _, ss in enumerate(result):
            try:
                output = frappe.get_print(doctype=doctype, name=ss, no_letterhead=no_letterhead, pdf_options=options)
            except Exception as e:
                frappe.log_error(
                    title="Error in PDF generation",
                    message=f"Error generating PDF for {ss} of doctype {doctype}: {str(e)}",
                    reference_doctype=doctype,
                    reference_name=ss,
                )

        filename = f"{doctype.replace(' ', '-').replace('/', '-')}.pdf"
    else:
        for doctype_name in doctype:
            for doc_name in doctype[doctype_name]:
                try:
                    output = frappe.get_print(
                        doctype_name,
                        doc_name,
                        format,
                        as_pdf=True,
                        output=output,
                        no_letterhead=no_letterhead,
                        letterhead=letterhead,
                        pdf_options=options,
                    )
                except Exception as e:
                    frappe.log_error(
                        title="Error in Multi PDF download",
                        message=f"Permission Error on doc {doc_name} of doctype {doctype_name}: {str(e)}",
                        reference_doctype=doctype_name,
                        reference_name=doc_name,
                    )

        filename = f"{name}.pdf"

    file_content = read_multi_pdf(output)

    if file_content:
        ret = frappe.get_doc({
            "doctype": "File",
            "attached_to_name": 'Report Dashboard',
            "attached_to_doctype": 'Report Dashboard',
            "attached_to_field": 'payslip',
            "file_name": filename,
            "is_private": 0,
            "content": file_content,
            "decode": False
        })
        ret.save(ignore_permissions=True)
        frappe.db.commit()

        attached_file = frappe.get_doc("File", ret.name)
        frappe.db.set_value('Report Dashboard', None, 'payslip', attached_file.file_url)
        frappe.db.set_value('Report Dashboard', None, 'last_download_on', now_datetime())

def read_multi_pdf(output):
    # Get the content of the merged pdf files
    fname = os.path.join("/tmp", f"frappe-pdf-{frappe.generate_hash()}.pdf")
    
    # Encode the string to bytes before writing
    with open(fname, "wb") as fileobj:
        fileobj.write(output.encode("utf-8"))

    with open(fname, "rb") as fileobj:
        filedata = fileobj.read()

    return filedata