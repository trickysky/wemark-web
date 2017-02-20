/**
 * Created by tk on 2017/1/3.
 */
var $factory_info_modal = $('#factory_info_modal'),
    $product_info = $('#product_info'),
    $product_image_modal = $('#product_image_modal'),
    $product_info_modal = $('#product_info_modal'),
    $company_info = $('#company_info');

$('#factory_info').find('.new-factory').bind('click', function () {
    init_modal();
    $factory_info_modal.modal('show');
});

$factory_info_modal.find('.confirm-btn').bind('click', function () {
    var factory_info = get_factory_info();
    if (factory_info.factory_name && factory_info.factory_type && factory_info.factory_ip && factory_info.factory_region && factory_info.factory_status && factory_info.factory_owner && factory_info.factory_phone && factory_info.factory_email) {
        $factory_info_modal.find('.modal-footer button').attr('disabled', true);
        $(this).html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>');
        $.ajax({
            type: 'POST',
            dateType: "json",
            url: "/s/factory",
            data: {
                'factory_name': factory_info['factory_name'],
                'location': factory_info['factory_ip'],
                'region': factory_info['factory_region'],
                'type': factory_info['factory_type'],
                'owner': factory_info['factory_owner'],
                'owner_email': factory_info['factory_email'],
                'owner_mobile': factory_info['factory_phone'],
                'status': factory_info['factory_status']
            },
            success: function (data) {
                if (data['code'] == 0) {
                    location.reload();
                }
            },
            error: function (xml, e) {
                $(this).html('提交');
                $('#factory_info_modal').find('.modal-footer button').attr('disabled', false);
                console.log('new factory: \r\n' + e);
            }
        })
    }
});

$('.drop-factory').bind('click', function () {
    var $this = $(this);
    var factory_id = $(this).attr('factory_id');
    if (factory_id) {
        $this.parent().html('<button type="button" class="btn btn-danger btn-xs confirm-delete-factory-btn">确认删除</button>');
        $('.confirm-delete-factory-btn').one('click', function () {
            $(this).html('<i class="fa fa-spinner fa-pulse fa-fw"></i>');
            $.ajax({
                type: 'DELETE',
                url: "/s/factory/" + factory_id,
                success: function (data) {
                    if (data['code'] == 0) {
                        $('#factory-' + factory_id).hide('slow');
                    }
                },
                error: function (xml, e) {
                    console.log('delete_factory error: \r\n '+e);
                }
            });
        });
    }
});


$('.update-factory').bind('click', function () {
    $factory_info_modal.find('.confirm-btn').addClass('hidden');
    $factory_info_modal.find('.update-btn').removeClass('hidden');
    var factory_id = $(this).attr('factory_id');
    var $factory_tr = $('#factory-' + factory_id);
    $('#factory_name').val($factory_tr.find('.td_factory_name').text());
    var factory_type = $factory_tr.find('.td_factory_type').text();
    var factory_type_val;
    var $factory_type = $('#factory_type');
    $factory_type.find('option').each(function () {
        if ($(this).text() == factory_type) {
            factory_type_val = $(this).val();
            return false;
        }
    });
    if (factory_type_val) {
        $factory_type.val(factory_type_val);
    }
    $factory_type.selectpicker('refresh');
    $('#factory_ip').val($factory_tr.find('.td_factory_ip').text());
    $('#factory_region').val($factory_tr.find('.td_factory_region').text());
    var factory_status = $factory_tr.find('.td_factory_status').text();
    var factory_status_val;
    var $factory_status = $('#factory_status');
    $factory_status.find('option').each(function () {
        if ($(this).text() == factory_status) {
            factory_status_val = $(this).val();
            return false;
        }
    });
    if (factory_status_val) {
        $factory_status.val(factory_status_val);
    }
    $factory_status.selectpicker('refresh');
    $('#factory_owner').val($factory_tr.find('.td_factory_owner').text());
    $('#factory_phone').val($factory_tr.find('.td_factory_owner_phone').text());
    $('#factory_email').val($factory_tr.find('.td_factory_owner_email').text());
    $factory_info_modal.factory_id = factory_id;
    $factory_info_modal.modal('show');
});


$factory_info_modal.find('.update-btn').on('click', function () {
    var factory_name = $('#factory_name').val();
    var factory_type = $('#factory_type').val();
    var factory_ip = $('#factory_ip').val();
    var factory_region = $('#factory_region').val();
    var factory_status = $('#factory_status').val();
    var factory_owner = $('#factory_owner').val();
    var factory_phone = $('#factory_phone').val();
    var factory_email = $('#factory_email').val();
    if (factory_name && factory_type && factory_ip && factory_region && factory_status && factory_owner && factory_phone && factory_email) {
        $factory_info_modal.find('.modal-footer button').attr('disabled', true);
        $(this).html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>');
        $.ajax({
            type: 'POST',
            dateType: "json",
            url: "/s/factory/" + $factory_info_modal.factory_id,
            data: {
                'factory_name': factory_name,
                'location': factory_ip,
                'region': factory_region,
                'type': factory_type,
                'owner': factory_owner,
                'owner_email': factory_email,
                'owner_mobile': factory_phone,
                'status': factory_status
            },
            success: function (data) {
                if (data['code'] == 0) {
                    location.reload();
                    show_msg('success', '修改成功');
                } else {
                    console.log(data['msg']);
                    show_msg('warning', '更新失败');
                }
            },
            error: function (xml, e) {
                $(this).html('提交');
                $('#factory_info_modal').find('.modal-footer button').attr('disabled', false);
                console.log('update factory error: \r\n' + e);
                show_msg('fatal', '更新失败');
            }
        })
    }
});


function init_modal() {
    $('#factory_name').val(null);
    var $factory_type = $('#factory_type');
    $factory_type.val(null);
    $factory_type.selectpicker('refresh');
    $('#factory_ip').val(null);
    $('#factory_region').val(null);
    var $factory_status = $('#factory_status');
    $factory_status.val(null);
    $factory_status.selectpicker('refresh');
    $('#factory_owner').val(null);
    $('#factory_phone').val(null);
    $('#factory_email').val(null);
    $factory_info_modal.find('.update-btn').addClass('hidden');
    $factory_info_modal.find('.confirm-btn').removeClass('hidden');
    $('#product_name').val(null);
    $('#product_unit').val(null);
    $('#product_barcode').val(null);
    $('#product_icon').val(null);
    $('#product_images').val(null);
    $('#product_intro').val(null);
    $('#product_description').val(null);
    $product_info_modal.find('.update-btn').addClass('hidden');
    $product_info_modal.find('.confirm-btn').removeClass('hidden');
}

function get_factory_info() {
    return {
        'factory_name': $('#factory_name').val(),
        'factory_type': $('#factory_type').val(),
        'factory_ip': $('#factory_ip').val(),
        'factory_region': $('#factory_region').val(),
        'factory_status': $('#factory_status').val(),
        'factory_owner': $('#factory_owner').val(),
        'factory_phone': $('#factory_phone').val(),
        'factory_email': $('#factory_email').val()
    };
}

$company_info.find('.tab-footer .confirm').bind('click', function () {
    var company_name = $company_info.find('#company_name').val();
    var company_description = $company_info.find('#company_description').val();
    var company_homepage = $company_info.find('#company_homepage').val();
    if (company_name) {
        $company_info.find('.tab-footer .confirm').html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>')
        $.ajax({
            type: 'POST',
            url: '/s/company',
            data: {
                'name': company_name,
                'description': company_description,
                'homepage': company_homepage
            },
            success: function (data) {
                if (0 == data['code']) {
                    location.reload();
                    show_msg('success', '修改成功');
                } else {
                    show_msg('warning', '更新失败！');
                    console.log(data['msg']);
                    $company_info.find('.tab-footer .confirm').html('提交更改')
                }
            },
            error: function (xml, e) {
                show_msg('fatal', '更新失败!');
                $company_info.find('.tab-footer .confirm').html('');
                console.log('update company error: \r\n'+e);
            }
        })
    }
});

function check_award_setting() {
    var total_prize = parseFloat($award_total_prize.val());
    var award_rate = parseFloat($award_rate.val());
    var min_prize = parseFloat($award_min_prize.val());
    var max_prize = parseFloat($award_max_prize.val());
    if (isNaN(total_prize) || isNaN(award_rate) || isNaN(min_prize) || isNaN(max_prize)) {
        $award_setting_confirm.attr('disabled', true);
    } else {
        $award_setting_confirm.attr('disabled', false);
    }
}

$product_info.find('.td-image').bind('click', function () {
    var image_url = $(this).find('img').attr('src');
    $product_image_modal.find('.modal-body img').attr('src', image_url);
    $product_image_modal.modal('show');
});

$product_info.find('.new-product').bind('click', function () {
    init_modal();
    $product_info_modal.modal('show');
});

function get_product_info() {
    return {
        'product_name': $('#product_name').val(),
        'product_unit': $('#product_unit').val(),
        'barcode': $('#product_barcode').val(),
        'product_icon': $('#product_icon').val(),
        'product_images': $('#product_images').val(),
        'product_intro': $('#product_intro').val(),
        'product_description': $('#product_description').val()
    };
}

$product_info_modal.find('.modal-footer .confirm-btn').bind('click', function () {
    var product_info = get_product_info();
    if (product_info.product_name) {
        $product_info_modal.find('.modal-footer .confirm-btn').html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>');
        $.ajax({
            type: 'POST',
            url: '/s/product',
            data: {
                'name': product_info.product_name,
                'unit': product_info.product_unit,
                'barcode': product_info.barcode,
                'icon': product_info.product_icon,
                'images': product_info.product_images,
                'intro': product_info.product_intro,
                'description': product_info.product_description
            },
            success: function (data) {
                if (data['code'] == 0) {
                    location.reload();
                }
            },
            error: function () {
                $product_info_modal.find('.modal-footer .confirm-btn').text('提交');
            }
        });
    }
});

$product_info.find('.drop-product').bind('click', function () {
    var $this = $(this);
    var product_id = $this.attr('product_id');
    if (product_id) {
        $this.parent().html('<button type="button" class="btn btn-danger btn-xs confirm-delete-product-btn">确认删除</button>');
        $('.confirm-delete-product-btn').one('click', function () {
            $(this).html('<i class="fa fa-spinner fa-pulse fa-fw"></i>');
            $.ajax({
                type: 'DELETE',
                url: "/s/product/" + product_id,
                success: function (data) {
                    if (data['code'] == 0) {
                        $('#product-' + product_id).hide('slow');
                    }
                },
                error: function (xml, e) {
                    console.log('delete product error: \r\n' + e);
                }
            });
        });
    }
});

$product_info.find('.update-product').bind('click', function () {
    $product_info_modal.find('.modal-footer .confirm-btn').addClass('hidden');
    $product_info_modal.find('.modal-footer .update-btn').removeClass('hidden');
    var $this = $(this),
        product_id = $this.attr('product_id'),
        $product_id = $('#product-'+product_id);
    var product_name = $product_id.find('.td-product-name').text(),
        product_unit = $product_id.find('.td-product-unit').text(),
        product_barcode = $product_id.find('.td-product-barcode').text(),
        product_icon = $product_id.find('.td-product-icon img').attr('src'),
        product_images = $product_id.find('.td-product-images img').attr('src'),
        product_intro = $product_id.find('.td-product-intro').text(),
        product_description = $product_id.find('.td-product-description').text();
    $('#product_name').val(product_name);
    $('#product_unit').val(product_unit);
    $('#product_barcode').val(product_barcode);
    $('#product_icon').val(product_icon);
    $('#product_images').val(product_images);
    $('#product_intro').val(product_intro);
    $('#product_description').val(product_description);
    $product_info_modal.product_id=product_id;
    $product_info_modal.modal('show');
});

$product_info_modal.find('.modal-footer .update-btn').bind('click', function () {
    var product_info = get_product_info();
    if (product_info.product_name) {
        $product_info_modal.find('.modal-footer .update-btn').html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>');
        $.ajax({
            type: 'POST',
            url: '/s/product/' + $product_info_modal.product_id,
            data:{
                'name': product_info.product_name,
                'unit': product_info.product_unit,
                'barcode': product_info.barcode,
                'icon': product_info.product_icon,
                'images': product_info.product_images,
                'intro': product_info.product_intro,
                'description': product_info.product_description
            },
            success: function (data) {
                if (data['code']==0) {
                    location.reload();
                } else {
                    $product_info_modal.find('.modal-footer .update-btn').text('提交');
                    console.log('update product info error:\r\n' + e);
                }
            },
            error: function (xml, e) {
                $product_info_modal.find('.modal-footer .update-btn').text('提交');
                console.log('update product info error:\r\n' + e);
            }
        });
    }
});
