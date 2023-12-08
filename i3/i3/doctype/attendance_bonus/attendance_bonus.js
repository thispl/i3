// frappe.ui.form.on('Attendance Bonus', {
//     from_date(frm) {
//         frappe.call({
//             method: 'i3.i3.doctype.attendance_bonus.attendance_bonus.get_end_date',
//             args: {
//                 frequency: "Monthly",
//                 start_date: frm.doc.from_date
//             },
//             callback: function (r) {
//                 if(frm.doc.attendance_bonus_monthly_once==1){
//                     if (r.message) {
//                         frm.set_value('to_date', r.message.end_date);
//                     }
//                   } 
//                 },
                
//             });
//         },    
//     });
        
//     attendance_bonus_yearly_once(frm) {
//         frappe.call({
//             method: 'i3.i3.doctype.attendance_bonus.attendance_bonus.get_to_date',
//             args: {
//                 frequency: "Yearly",
//                 start_date: frm.doc.from_date
//             },
//             callback: function (r) {
//                 if(frm.doc.attendance_bonus_yearly_once==1){
//                     if (r.message) {
//                         frm.set_value('to_date', r.message.end_date);
//                     }
//                   } 
//                 }
// //             });
//         },    
//     });