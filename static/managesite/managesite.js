/**
 * Created by tk on 2016/11/26.
 */

$("#date_picker").datetimepicker({
    format: "yyyy年mm月dd日",
    showMeridian: true,
    todayBtn: true,
    language: "zh-CN",
    startDate: (new Date()).toISOString().substring(0, 10),
    autoclose: true,
    minView: "month",
    todayHighlight: true
});

$("#new_order_modal").find(".check-factory").find("input").change(function () {
    if($(this).is(":checked")) {
        $(this).parent(".code_factory").removeClass("disabled-font");
        $(this).parent(".code_factory").parent(".check-factory").find(".selectpicker").attr("disabled", false).selectpicker('refresh');
    }
    else {
        $(this).parent(".code_factory").addClass("disabled-font");
        $(this).parent(".code_factory").parent(".check-factory").find(".selectpicker").attr("disabled", true).selectpicker('refresh');
    }
});

$("#make_order_btn").bind("click", function () {
    $("#step1-body").hide(800);
    $("#step2-body").removeClass("hidden");
    $("#step2-foot").removeClass("hidden");
    $("#step1-foot").addClass("hidden");
    var datetime = $("#date_picker").val();
    if (datetime) {
        $("#batch_date").find(".batch-value").text(datetime);
    }
});

$("#back_btn").bind("click", function () {
    $("#step2-body").addClass("hidden");
    $("#step1-body").show();
    $("#step1-foot").removeClass("hidden");
    $("#step2-foot").addClass("hidden");
});