# coding=utf8
# Create your views here.
from collections import defaultdict

from django.shortcuts import render

from wemark.commons.response import ResponseEntity
from services import ReportService
from oauth2.commons.security import Subject


def set_index(request):
    service = create_service(request=request)

    base_data = {
        'app_name': u'数据报表',
        'icon_name': u'icon-bar-chart',
        'page_name': u'数据报表',
        'page_desc': u'图表-地图',
        'dashboards': get_dashboard(request).values(),
        'portlets': get_charts().values(),
        'dropdown_name': u'选择批次',
        'items': [{'id': bid, 'name': u'生产批次' + str(bid)} for bid in service.get_batches_ids()]
    }

    return base_data


def get_dashboard(request):
    service = create_service(request=request)
    ids = service.get_batches_ids()
    current_bid = ids[0] if len(ids) != 0 else None

    confs = defaultdict(dict)
    confs[0] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'blue', 'icon': 'bar-chart',
                'id': 'total_scan', 'name': u'总扫码量',
                'value': service.get_total_scan_count(current_bid) if current_bid is not None else 0}
    confs[1] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'yellow-crusta', 'icon': 'clock-o',
                'id': 'total_code', 'name': u'总赋码数',
                'value': service.get_total_code_count(current_bid) if current_bid is not None else 0}
    confs[2] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'green-jungle', 'icon': 'plug',
                'id': 'total_award', 'name': u'总奖金', 'value': service.get_total_award_amount(), 'unit': u'元'}
    confs[3] = {'lg_pos': 3, 'md_pos': 3, 'sm_pos': 6, 'xm_pos': 12, 'color': 'red', 'icon': 'exclamation-triangle',
                'id': 'total_accepted', 'name': u'已兑奖金额',
                'value': service.get_total_accepted_amount(current_bid) if current_bid is not None else 0, 'unit': u'元'}
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


def index(request):
    return render(request, 'report/index.html', set_index(request))


def scan_count(request, bid):
    service = create_service(request)
    return ResponseEntity.ok(service.get_total_scan_count(bid=bid))


def code_count(request, bid):
    service = create_service(request)
    return ResponseEntity.ok(service.get_total_code_count(bid=bid))


def award_amount(request):
    service = create_service(request)
    return ResponseEntity.ok(service.get_total_award_amount())


def accepted_amount(request, bid):
    service = create_service(request)
    return ResponseEntity.ok(service.get_total_accepted_amount(bid=bid))


def batch_id(request):
    service = create_service(request)
    return ResponseEntity.ok(service.get_batches_ids())


def daily_count(request, bid):
    service = create_service(request)
    return ResponseEntity.ok(service.get_daily_scan_and_accepted_count(bid=bid))


def accepted_rate(request):
    service = create_service(request)
    return ResponseEntity.ok(service.get_accepted_rate_by_product())


def create_service(request):
    subject = Subject.get_instance(request.session)
    return ReportService(user_id=subject.get_user_info()['id'], is_root=subject.has_role('root'))
