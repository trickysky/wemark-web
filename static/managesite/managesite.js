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

function refresh_total_count() {
    var $box_count = $("#box_count");
    var $bottle_count = $("#bottle_count");
    var box_count = $box_count.val();
    var bottle_count = $bottle_count.val();
    if (!isNaN(box_count) && !isNaN(bottle_count)) {
        $("#total_count").val(box_count * bottle_count);
    }
}

$("#box_count").bind('input', refresh_total_count);
$("#bottle_count").bind('input', refresh_total_count);

$("#total_count_checkbox").change(function () {
    var $box_count = $("#box_count");
    var $bottle_count = $("#bottle_count");
    if($(this).is(":checked")) {
        $box_count.val(0);
        $box_count.attr('disabled', true);
        $bottle_count.val(0);
        $bottle_count.attr('disabled', true);
        $("#total_count").attr('disabled', false);
    } else {
        $box_count.attr('disabled', false);
        $bottle_count.attr('disabled', false);
        $("#total_count").attr('disabled', true);
    }
});


$("#make_order_btn").bind("click", function () {
    $("#step1-body").hide();
    $("#step2-body").removeClass("hidden");
    $("#step2-foot").removeClass("hidden");
    $("#step1-foot").addClass("hidden");

    // 时间
    var datetime = $("#date_picker").val();
    if (datetime) {
        var $batch_date_value = $("#batch_date").find(".batch-value");
        $batch_date_value.text(datetime);
        $batch_date_value.removeClass('red-font');
    }

    // 产品条码
    var barcode = $("#barcode").find("option:selected").text();
    var $batch_barcode_value = $("#batch_barcode").find(".batch-value");
    if (barcode && barcode != '-') {
        $batch_barcode_value.text(barcode);
        $batch_barcode_value.removeClass('red-font');
    }
    else if (barcode == '-') {
        $batch_barcode_value.text('未设置');
        $batch_barcode_value.addClass('red-font');
    }

    // 激活工厂
    var factory = $("#factory").find("option:selected").text();
    var $batch_factory_value = $("#batch_factory").find(".batch-value");
    if (factory && factory != '-') {
        $batch_factory_value.text(factory);
        $batch_factory_value.removeClass('red-font');
    }
    else if (factory == '-') {
        $batch_factory_value.text('未设置');
        $batch_factory_value.addClass('red-font');
    }

    // 生产数量
    var $box_count = $("#box_count");
    var $bottle_count = $("#bottle_count");
    var $total_count = $("#total_count");
    var box_count = $box_count.val();
    var bottle_count = $bottle_count.val();
    var total_count = $total_count.val();
    var $batch_count_value = $("#batch_count").find(".batch-value");
    if ($total_count.attr("disabled")) {
        if (box_count>0 && bottle_count>0) {
            $batch_count_value.text(box_count+"万箱"+" X "+bottle_count+"瓶/箱 = "+box_count*bottle_count+'万瓶');
            $batch_count_value.removeClass('red-font');
        }
        else {
            $batch_count_value.text("未设置");
            $batch_count_value.addClass("red-font");
        }
    }
    else {
        if (total_count>0) {
            $batch_count_value.text(total_count+'万瓶');
            $batch_count_value.removeClass('red-font');
        }
        else {
            $batch_count_value.text("未设置");
            $batch_count_value.addClass("red-font");
        }
    }
});

$("#back_btn").bind("click", function () {
    $("#step2-body").addClass("hidden");
    $("#step1-body").show();
    $("#step1-foot").removeClass("hidden");
    $("#step2-foot").addClass("hidden");
});