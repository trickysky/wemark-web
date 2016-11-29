/**
 * Created by tk on 2016/11/26.
 */

$("#newOrderModal").modal('show');
$("#datePicker").datetimepicker({
    format: "yyyy年mm月dd日",
    showMeridian: true,
    todayBtn: true,
    language: "zh-CN",
    startDate: (new Date()).toISOString().substring(0, 10),
    autoclose: true,
    minView: "month",
    todayHighlight: true
});


