/**
 * Created by tk on 2016/11/26.
 */

$("#new_order_modal").find(".check-factory").find("input").change(function () {
    if ($(this).is(":checked")) {
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
    var box_count_unit = $("#box_count_unit").val();
    var is_total_count_checked = $("#total_count_checkbox").is(":checked");
    $("#total_count_unit").selectpicker('val', '1');
    if (!is_total_count_checked && !isNaN(box_count) && !isNaN(bottle_count)) {
        $("#total_count").val(box_count * bottle_count * box_count_unit);
    }
}

$("#box_count").bind('input', refresh_total_count);
$("#bottle_count").bind('input', refresh_total_count);
$("#box_count_unit").bind('change', refresh_total_count);

$("#total_count_checkbox").change(function () {
    var $box_count = $("#box_count");
    var $bottle_count = $("#bottle_count");
    if ($(this).is(":checked")) {
        $box_count.val(0);
        $box_count.attr('disabled', true);
        $bottle_count.val(0);
        $bottle_count.attr('disabled', true);
        $("#total_count").attr('disabled', false);
        $("#total_count_unit").attr('disabled', false).selectpicker('refresh');
    } else {
        $box_count.attr('disabled', false);
        $bottle_count.attr('disabled', false);
        $("#total_count").attr('disabled', true);
        $("#total_count_unit").attr('disabled', true).selectpicker('refresh');
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
        var now = new Date();
        var period = new Date(now.setMonth(parseInt(now.getMonth()) + parseInt(datetime)));
        $batch_date_value.text(period.getFullYear() + '/' + (period.getMonth() + 1) + '/' + period.getDate());
        $batch_date_value.removeClass('red-font');
    }

    // 产品名称
    var prod_name = $("#product").find("option:selected").text();
    var $batch_prod_value = $("#batch_prod_name").find(".batch-value");
    if (prod_name && prod_name != '-') {
        $batch_prod_value.text(prod_name);
        $batch_prod_value.removeClass('red-font');
    }
    else if (prod_name == '-') {
        $batch_prod_value.text('未设置');
        $batch_prod_value.addClass('red-font');
    }

    // 激活工厂
    var factory = $("#factory").find("option:selected").text();
    var $batch_factory_value = $("#batch_factory").find(".batch-value");
    $batch_factory_value.text(factory);
    $batch_factory_value.removeClass('red-font');

    // 生产数量
    var $box_count = $("#box_count");
    var $box_count_unit = $("#box_count_unit");
    var $bottle_count = $("#bottle_count");
    var $total_count = $("#total_count");
    var $total_count_unit = $("#total_count_unit");
    var box_count = $box_count.val();
    var box_count_unit = $box_count_unit.val();
    var bottle_count = $bottle_count.val();
    var total_count_unit = $("#total_count_unit").val();
    var total_count = $total_count.val();
    var $batch_count_value = $("#batch_count").find(".batch-value");
    var box_count_unit_text = $box_count_unit.find("option:selected").text();
    var total_count_unit_text = $total_count_unit.find("option:selected").text();
    if ($total_count.attr("disabled")) {
        if (box_count>0 && bottle_count>0) {
            $batch_count_value.text(box_count * box_count_unit + box_count_unit_text + " X " + bottle_count + "瓶/箱 = " + total_count + total_count_unit_text);
            $batch_count_value.removeClass('red-font');
        }
        else {
            $batch_count_value.text("未设置");
            $batch_count_value.addClass("red-font");
        }
    }
    else {
        if (total_count>0) {
            $batch_count_value.text(total_count * total_count_unit + "瓶");
            $batch_count_value.removeClass('red-font');
        }
        else {
            $batch_count_value.text("未设置");
            $batch_count_value.addClass("red-font");
        }
    }

    // 内码赋码工厂
    var $batch_inner_code = $("#batch_inner_code").find(".batch-value");
    var $inner_code = $("#inner_code");
    if ($inner_code.find(".code_factory").hasClass("disabled-font")) {
        $batch_inner_code.text("未设置");
        $batch_inner_code.addClass("red-font");
    }
    else {
        var inner_code = $inner_code.find("option:selected").text();
        $batch_inner_code.text(inner_code);
        $batch_inner_code.removeClass("red-font");
    }

    // 外码赋码工厂
    var $batch_outer_code = $("#batch_outer_code").find(".batch-value");
    var $outer_code = $("#outer_code");
    if ($outer_code.find(".code_factory").hasClass("disabled-font")) {
        $batch_outer_code.text("未设置");
        $batch_outer_code.addClass("red-font");
    }
    else {
        var outer_code = $outer_code.find("option:selected").text();
        $batch_outer_code.text(outer_code);
        $batch_outer_code.removeClass("red-font");
    }

    // 箱码赋码工厂
    var $batch_box_code = $("#batch_box_code").find(".batch-value");
    var $box_code = $("#box_code");
    if ($box_code.find(".code_factory").hasClass("disabled-font")) {
        $batch_box_code.text("未设置");
        $batch_box_code.addClass("red-font");
    }
    else {
        var box_code = $box_code.find("option:selected").text();
        $batch_box_code.text(box_code);
        $batch_box_code.removeClass("red-font");
    }

    //产品信息
    var $prod_info = $("#prod_info");
    var prod_info = $prod_info.val();
    var $batch_prod_info_value = $("#batch_prod_info").find(".batch-value");
    if (prod_info) {
        $batch_prod_info_value.text(prod_info);
        $batch_prod_info_value.removeClass("red-font");
    } else {
        $batch_prod_info_value.text("未设置");
        $batch_prod_info_value.addClass("red-font");
    }

    // 产品条码
    var barcode = (function () {
        try {
            return JSON.parse(prod_info)["barcode"];
        } catch (e) {
            return undefined;
        }
    })();
    var $batch_barcode_value = $("#batch_barcode").find(".batch-value");
    if (barcode) {
        $batch_barcode_value.text(barcode);
        $batch_barcode_value.removeClass('red-font');
    }
    else {
        $batch_barcode_value.text('无');
        $batch_barcode_value.addClass('red-font');
    }
});

$("#back_btn").bind("click", function () {
    $("#step2-body").addClass("hidden");
    $("#step1-body").show();
    $("#step1-foot").removeClass("hidden");
    $("#step2-foot").addClass("hidden");
});

var $confirm_btn = $("#confirm_btn");
$confirm_btn.bind("click", function () {
    var now = new Date();
    var datetime = new Date(now.setMonth(parseInt(now.getMonth() + parseInt($("#date_picker").val())))).getTime();
    var prod_id = $("#product").find("option:selected").val();
    if (!prod_id) {
        prod_id = undefined;
    }
    var factory_id = parseInt($("#factory").find("option:selected").val());
    var box_count = $("#box_count").val();
    var box_count_unit = $("#box_count_unit").val();
    var bottle_count = $("#bottle_count").val();
    var $total_count = $("#total_count");
    var total_count = $total_count.val() * $("#total_count_unit").val();
    if (!$total_count.attr("disabled")) {
        box_count = undefined;
        bottle_count = undefined;
    }

    var $inner_code = $("#inner_code");
    var inner_code_factory_id;
    if (!$inner_code.find(".code_factory").hasClass("disabled-font")) {
        inner_code_factory_id = parseInt($inner_code.find("option:selected").val());
    }

    var $outer_code = $("#outer_code");
    var outer_code_factory_id;
    if (!$outer_code.find(".code_factory").hasClass("disabled-font")) {
        outer_code_factory_id = parseInt($outer_code.find("option:selected").val());
    }

    var $box_code = $("#box_code");
    var box_code_factory_id;
    if (!$box_code.find(".code_factory").hasClass("disabled-font")) {
        box_code_factory_id = parseInt($box_code.find("option:selected").val());
    }
    var prod_info = $("#prod_info").val();
    var barcode = (function () {
        try {
            return JSON.parse(prod_info)["barcode"];
        } catch (e) {
            return undefined;
        }
    })();

    var generate_code = inner_code_factory_id || outer_code_factory_id || box_code_factory_id;
    if (factory_id && total_count && datetime && prod_id && generate_code) {
        $confirm_btn.html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>');
        $confirm_btn.attr("disabled", true);
        $("#back_btn").attr("disabled", true);
        $.ajax({
            type: "POST",
            dateType: "json",
            url: "s/batch",
            data: {
                'factory_id': factory_id,
                'barcode': barcode,
                'incode_factory': inner_code_factory_id,
                'outcode_factory': outer_code_factory_id,
                'casecode_factory': box_code_factory_id,
                'case_count': box_count,
                'case_size': bottle_count,
                'unit_count': total_count,
                'product_id': prod_id,
                'expired_time': datetime,
                'product_info': prod_info
            },
            success: function (data) {
                if (data['code'] == 0) {
                    console.log('post success');
                    location.reload();
                }
            },
            error: function (xml, e) {
                $confirm_btn.html('确认提交');
                $confirm_btn.attr("disabled", false);
                $("#back_btn").attr("disabled", false);
                console.log(e);
            }
        });
    }
});

$('#product').bind('change', function () {
    var product_id = $(this).val();
    if (product_id) {
        $.ajax({
            type: 'GET',
            url: '/s/product/' + product_id,
            success: function (data) {
                if (data['code'] == 0) {
                    $('#prod_info').val(JSON.stringify(data['data'], undefined, 4));
                }
            },
            error: function (xml, e) {
                console.log('get product error: \r\n' + e);
            }
        });
        // refresh the product unit
        var unit = $("#product_" + product_id).text();
        $(".product_unit").html(unit);
    }
});

$('.base_count_options>li>a').bind('click', function () {
    var target = $(this).parents("div.dropdown").find("span.base_count");
    var value = $(this).attr("value");
    var content = $(this).html();
    if (value != target.attr("value")) {
        target.attr("value", value).html(content);
        refresh_total_count();
    }
});

$('a.download_code').bind('click', function () {
    var code_type = $(this).attr('code-type');
    var batch_id = $(this).parents('.batch-list-item').attr("value");
    var radio_name = code_type + '_download_type_' + batch_id;
    var csv_type = $("input[name=" + radio_name + "]:checked").val() == 'csv';
    $.ajax({
        type: 'POST',
        url: 's/batch/download_code',
        data: {
            'code_type': code_type,
            'batch_id': batch_id,
            'csv_type': csv_type
        },
        success: function (data, status, request) {
            var DEFAULT_CODE_DOWNLOAD_LIMIT = 1000;
            var disp = request.getResponseHeader('Content-Disposition');
            if (data['error_code'] == 0) {
                var url_list = data['data'];
                if (url_list.length > DEFAULT_CODE_DOWNLOAD_LIMIT) {
                    $('#downloadModal').modal();
                    return;
                }
                var render_type = code_type == 'inner' ? 'qr' : 'dm';
                create_code_pic_and_download(url_list, render_type);
            } else if (disp && disp.search('attachment') != -1) {
                var form = $('<form method="POST" action="s/batch/download_code">');
                form.append($('<input type="hidden" name="batch_id" value="' + batch_id + '">'));
                form.append($('<input type="hidden" name="code_type" value="' + code_type + '">'));
                form.append($('<input type="hidden" name="csv_type" value="' + csv_type + '">'));
                $('body').append(form);
                form.submit();
            } else {
                console.log('download code failed: ' + data);
                show_msg('warning', '下载失败');
            }
        },
        error: function (xml, e) {
            console.log('get product error: \r\n' + e);
            show_msg('warning', '下载失败');
        }
    });

});

$('a.send_code').bind('click', function () {
    var factory_id = $(this).attr('value');
    var code_type = $(this).attr('code-type');
    var batch_id = $(this).parents('.batch-list-item').attr("value");
    $.ajax({
        type: 'POST',
        url: 's/batch/send_code',
        data: {
            'factory_id': factory_id,
            'code_type': code_type,
            'batch_id': batch_id
        },
        success: function (data) {
            if (!data || data['code'] != 0) {
                console.log('send code failed: ' + data);
                show_msg('warning', '发送失败');
            } else {
                show_msg('success', '发送成功');
            }
        },
        error: function (xml, e) {
            console.log('get product error: \r\n' + e);
            show_msg('warning', '发送失败');
        }
    });
});

$('a.enable_code').bind('click', function () {
    var batch_list_item = $(this).parents('.batch-list-item');
    var factory_id = $(this).attr('value');
    var batch_id = batch_list_item.attr("value");
    $.ajax({
        type: 'POST',
        url: 's/batch/enable_code',
        data: {
            'factory_id': factory_id,
            'batch_id': batch_id
        },
        success: function (data) {
            if (data && data['code'] == 0) {
                show_msg('success', '激活成功');
                reload_batch_item(batch_list_item);
            }
        },
        error: function (xml, e) {
            console.log('enable code error: \r\n' + e);
            show_msg('warning', '激活失败');
        }
    });
});

function reload_batch_item(batch_item) {
    $.ajax({
        type: 'GET',
        url: 's/batch/' + batch_item.attr('value'),
        success: function (data) {
            if (data && data['code'] == 0) {
                if (data['data'].status != 2) {
                    batch_item.find('li:not(.enabled-factory)>span.label').remove();
                    if (data['data'].status == 0) {
                        batch_item.find('li.enabled-factory>span.label')
                            .removeClass('label-default')
                            .addClass('label-success')
                            .html(' 已激活 ');
                    }
                }
            }
        },
        error: function (xml, e) {
            console.log('get batch info error: \r\n' + e);
        }
    });
}

function create_code_pic_and_download(urls, code_type) {
    var margin, code_size;
    var canvas = $("#qrdm");
    var canvas_element = document.getElementById("qrdm");
    canvas.clearCanvas();

    function renderQRCode() {
        var code_per_row = 4;
        margin = 50;
        code_size = 200;

        var row_number = Math.ceil(urls.length / code_per_row);
        var width = code_per_row * code_size + (code_per_row + 1) * margin;
        var height = row_number * code_size + (row_number + 1) * margin;

        canvas_element.width = width;
        canvas_element.height = height;

        var top = margin, left = margin;
        for (var idx = 0; idx < urls.length; ++idx) {
            var url = urls[idx];
            var option = {
                text: url.trim(),
                render: "canvas",
                size: code_size,
                background: 'white',
                mode: 0,
                minVersion: 1,
                maxVersion: 3,
                ecLevel: "L",
                left: left,
                top: top
            };
            canvas.qrcode(option);
            left += code_size + margin;
            if (left > width - code_size - margin) {
                left = margin;
                top += code_size + margin;
            }
            if (top > height - code_size - margin) {
                break
            }
        }
    }

    function renderDMCode() {
        var code_per_row = 8;
        margin = 25;
        code_size = 100;
        var canvas = $("#qrdm");
        var row_number = Math.ceil(urls.length / code_per_row);
        var width = code_per_row * code_size + (code_per_row + 1) * margin;
        var height = row_number * code_size + (row_number + 1) * margin;

        var canvas_element = document.getElementById("qrdm");
        canvas_element.width = width;
        canvas_element.height = height;

        canvas.clearCanvas();
        var top = margin, left = margin;
        for (var idx = 0; idx < urls.length; ++idx) {
            var url = urls[idx];
            var option = {
                output: "canvas",
                barWidth: code_size,
                barHeight: code_size,
                background: 'white',
                showURI: true,
                posX: left,
                posY: top
            };
            canvas.barcode(url.trim(), "datamatrix", option);
            left += code_size + margin;
            if (left > width - code_size - margin) {
                left = margin;
                top += code_size + margin;
            }
            if (top > height - code_size - margin) {
                break
            }
        }
    }

    if (code_type == 'qr') {
        renderQRCode()
    } else if (code_type == 'dm') {
        renderDMCode()
    }

    var fixTypeFun = function (type) {
        type = type.toLowerCase().replace(/jpg/i, 'jpeg');
        var r = type.match(/png|jpeg|bmp|gif/)[0];
        return 'image/' + r;
    };

    var type = 'png';
    var img_data = (canvas[0]).toDataURL(type);
    img_data = img_data.replace(fixTypeFun(type), 'image/octet-stream');
    var link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
    link.href = img_data;
    link.download = code_type + '_code_' + new Date().getTime().toString() + '.' + type;

    var event = document.createEvent('MouseEvents');
    event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    link.dispatchEvent(event);
}
