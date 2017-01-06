/**
 * Created by tk on 2017/1/3.
 */

$('#factory_info_modal').find('.confirm_btn').bind('click', function () {
    var factory_name = $('#factory_name').val();
    var factory_type = $('#factory_type').val();
    var factory_ip = $('#factory_ip').val();
    var factory_region = $('#factory_region').val();
    var factory_status = $('#factory_status').val();
    var factory_owner = $('#factory_owner').val();
    var factory_phone = $('#factory_phone').val();
    var factory_email = $('#factory_email').val();
    if (factory_name && factory_type && factory_ip && factory_region && factory_status && factory_owner && factory_phone && factory_email) {
        $('#factory_info_modal').find('.modal-footer button').attr('disabled', true);
        $(this).html('发送中<i class="fa fa-spinner fa-pulse fa-fw"></i>');
        $.ajax({
            type: 'POST',
            dateType: "json",
            url: "/s/factory",
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
                if (data['code']==0) {
                    location.reload();
                }
            },
            error: function (xml, e) {
                $(this).html('提交');
                $('#factory_info_modal').find('.modal-footer button').attr('disabled', false);
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
                    console.log('delete_factory error');
                }
            });
        });
    }
});


$('.update-factory').bind('click', function () {
    var factory_id = $(this).attr('factory_id');
    var $factory_tr = $('#factory-' + factory_id);
    $('#factory_name').val($factory_tr.find('.td_factory_name').text());
    var factory_type = $factory_tr.find('.td_factory_type').text();
    var factory_type_val;
    var $factory_type = $('#factory_type');
    $factory_type.find('option').each(function () {
        console.log($(this).text());
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
        console.log($(this).text());
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
    $('#factory_info_modal').modal('show');
});


function init_modal() {

}