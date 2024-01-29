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
    else if (frm.doc.report == 'BOT Report') {
        var path = "i3.i3.doctype.report_dashboard.bot_report.download"
        var args = 'employee=%(employee)s&from_date=%(from_date)s&to_date=%(to_date)s'		
    }
    else if (frm.doc.report == 'Bank Remittance Report') {
        var path = "i3.i3.doctype.report_dashboard.bank_remittance_report_with_customer_wise.download"
        var args = 'employee=%(employee)s&customer=%(customer)s&from_date=%(from_date)s&to_date=%(to_date)s'		
    }


    if (path) {
        window.location.href = repl(frappe.request.url +
            '?cmd=%(cmd)s&%(args)s', {
            cmd: path,
            args: args,
            from_date : frm.doc.from_date,
            to_date : frm.doc.to_date,
            employee : frm.doc.employee,
            customer:frm.doc.customer
            
        });
    }
    }
});
