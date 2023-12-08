// Copyright (c) 2023, Narayanan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
    download:function(frm){
    if (frm.doc.report == 'Payslip') {
        if(frm.doc.from_date && frm.doc.to_date){
        frappe.call({
            method:"i3.i3.doctype.report_dashboard.payslip_print.enqueue_download_multi_pdf",
            args:{
                doctype:"Payslip",
                customer:frm.doc.customer,
                employee:frm.doc.employee,
                start_date: frm.doc.from_date,
                end_date: frm.doc.to_date		
            },
            callback(r){
                if(r){
                    console.log(r)
                }
            }
        })
        }
    }
}
});
