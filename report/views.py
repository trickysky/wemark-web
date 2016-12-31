# coding=utf8
# Create your views here.
from collections import defaultdict

from django.shortcuts import render

from services.award import AwardService
from services.batch import BatchService
from services.scan_code import ScanCodeService
from wemark.commons.response import ResponseEntity

award_service = AwardService()
scan_code_service = ScanCodeService()
batch_service = BatchService()


def set_index():
    base_data = {
        'app_name': u'数据报表',
        'icon_name': u'icon-bar-chart',
        'page_name': u'数据报表',
        'page_desc': u'图表-地图',
        'dashboards': get_dashboard().values(),
        'portlets': get_charts().values()
    }

    return base_data


def get_dashboard():
    confs = defaultdict(dict)
    confs[0] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'blue', 'icon': 'bar-chart',
                'name': u'总扫码量', 'value': u'1,209,437'}
    confs[1] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'yellow-crusta', 'icon': 'clock-o',
                'name': u'总赋码数', 'value': u'10,261,034'}
    confs[2] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'green-jungle', 'icon': 'plug',
                'name': u'总奖金', 'value': u'5,000,000', 'unit': u'元'}
    confs[3] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'red', 'icon': 'exclamation-triangle',
                'name': u'已兑奖金额',
                'value': u'1,146,302', 'unit': u'元'}
    return confs


def get_charts():
    confs = defaultdict(dict)
    confs[0] = {'lg_pos': 6, 'md_pos': 12, 'sm_pos': 12, 'xm_pos': 12, 'icon': 'line-chart', 'icon_color': 'green-haze',
                'font_color': 'green-haze', 'name': u'用户趋势', 'desc': u'扫码数、兑奖数趋势',
                'actions': "brief/trend_actions.html", 'body_id': 'datatrend', 'body_class': 'CSSAnimationChart'}
    confs[1] = {'lg_pos': 6, 'md_pos': 12, 'sm_pos': 12, 'xm_pos': 12, 'icon': 'calendar', 'icon_color': 'red-sunglo',
                'font_color': 'red-sunglo', 'name': u'区域分布', 'desc': u'用户扫码地点分布',
                'actions': "brief/balance_actions.html", 'body_id': 'spiderbalance', 'body_class': 'CSSAnimationChart'}
    confs[2] = {'lg_pos': 6, 'md_pos': 12, 'sm_pos': 12, 'xm_pos': 12, 'icon': 'pie-chart', 'icon_color': 'yellow',
                'font_color': 'yellow', 'name': u'产品类型', 'desc': u'不同产品的兑奖率',
                'actions': "brief/filter_order_actions.html", 'body_id': 'datarank', 'body_class': 'CSSAnimationChart'}
    confs[3] = {'lg_pos': 6, 'md_pos': 12, 'sm_pos': 12, 'xm_pos': 12, 'icon': 'list-ol',
                'icon_color': 'purple-sharp', 'font_color': 'purple-sharp', 'name': u'奖池状态', 'desc': u'显示奖池兑奖情况',
                'actions': "brief/filter_actions.html", 'body_id': 'dataformation', 'body_class': 'CSSAnimationChart'}
    return confs


def fetch_batches_if_necessary(start_ts, end_ts, force_update):
    success = True
    error_message = None

    if force_update or not batch_service.has_cache(BatchService.CACHE_BATCH_IDS_KEY):
        success = batch_service.fetch(start_ts, end_ts)
        error_message = batch_service.get_error_message()

    return success, error_message


def index(request):
    return render(request, 'report/index.html', set_index())


def scan_code(request):
    start_ts, end_ts, force_update = get_params(request.GET)
    success = True
    error_message = None

    if force_update or not scan_code_service.has_cache(ScanCodeService.CACHE_SCAN_CODE_COUNT_KEY):
        success, error_message = fetch_batches_if_necessary(start_ts, end_ts, error_message)

        if success:
            batch_ids = batch_service.get_batch_ids()
            success = scan_code_service.fetch_all(batch_ids=batch_ids, location=None, start_time=start_ts,
                                                  end_time=end_ts)
            error_message = scan_code_service.get_error_message()

    return ResponseEntity.ok(scan_code_service.get_scan_count()) if success else ResponseEntity.bad_request(
        error_message)


def award_amount(request):
    start_ts, end_ts, force_update = get_params(request.GET)
    success = True
    error_message = None

    if force_update or not award_service.has_cache(AwardService.CACHE_AWARD_AMOUNT_KEY):
        success, error_message = fetch_batches_if_necessary(start_ts, end_ts, force_update)

        if success:
            batch_ids = batch_service.get_batch_ids()
            success = award_service.fetch_all(batch_ids=batch_ids, accept_location=None, start_accept_time=start_ts,
                                              end_accept_time=end_ts)
            error_message = award_service.get_error_message()

    return ResponseEntity.ok(award_service.get_award_amount()) if success else ResponseEntity.bad_request(error_message)


def award_count(request):
    start_ts, end_ts, force_update = get_params(request.GET)
    success = True
    error_message = None

    if force_update or not award_service.has_cache(AwardService.CACHE_AWARD_COUNT_KEY):
        success, error_message = fetch_batches_if_necessary(start_ts, end_ts, force_update)

        if success:
            batch_ids = batch_service.get_batch_ids()
            success = award_service.fetch_all(batch_ids=batch_ids, accept_location=None, start_accept_time=start_ts,
                                              end_accept_time=end_ts)
            error_message = award_service.get_error_message()

    return ResponseEntity.ok(award_service.get_award_count()) if success else ResponseEntity.bad_request(error_message)


def get_params(params):
    start_ts = params.get('start_ts')
    end_ts = params.get('start_ts')
    if start_ts is not None and start_ts.isdigit():
        start_ts = long(start_ts)
    if end_ts is not None and end_ts.isdigit():
        end_ts = long(end_ts)
    force_update = params.get('force_update')
    if force_update is None:
        force_update = False
        return start_ts, end_ts, force_update
