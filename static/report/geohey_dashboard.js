/**
 * Created by Nathan on 12/28/15.
 * Optimize by TK on 1/14/16
 */

var dashboard = function () {
    return {
        initDataTrend: function (data) {
            if (typeof(AmCharts) === 'undefined' || $('#datatrend').size() === 0) {
                return;
            }

            var chart = AmCharts.makeChart("datatrend", {
                "type": "serial",
                "categoryField": "date",
                "dataDateFormat": "YYYY-MM-DD",
                "startDuration": 1,
                "export": {
                    "enabled": true
                },
                "startEffect": "easeInSine",
                "categoryAxis": {
                    "gridPosition": "start",
                    "parseDates": true
                },
                "chartCursor": {
                    "enabled": true,
                    "categoryBalloonDateFormat": "MMM DD"
                },
                "trendLines": [],
                "graphs": [
                    {
                        "accessibleLabel": "[[title]] : [[value]]",
                        "balloonText": "[[title]] : [[value]]",
                        "bullet": "round",
                        "id": "AmGraph-1",
                        "labelText": "",
                        "lineAlpha": 0.87,
                        "lineThickness": 3,
                        "showAllValueLabels": true,
                        "title": "扫码数",
                        "valueField": "scan"
                    },
                    {
                        "accessibleLabel": "[[title]] : [[value]]",
                        "balloonText": "[[title]] : [[value]]",
                        "fillAlphas": 0.7,
                        "id": "AmGraph-2",
                        "labelText": "[[value]]",
                        "title": "兑奖数",
                        "type": "column",
                        "valueField": "confirm"
                    }
                ],
                "guides": [],
                "valueAxes": [
                    {
                        "id": "ValueAxis-1",
                        "title": "次数"
                    }
                ],
                "allLabels": [],
                "balloon": {},
                "legend": {
                    "enabled": true,
                    "align": "center",
                    "position": "top",
                    "valueAlign": "left"
                },
                "titles": [],
                "dataProvider": data
            });
        },
        initSpiderBalance: function () {
            $('#spiderbalance').html("<iframe width=100% height=100% src='http://geohey.com/apps/dataviz/55f5f8c6105143bd989a7c42a4f12b19/share?ak=N2IxMTc3MTIyODRlNGJkNjkxYWVlNDQ4OWI1YWY0ZTk' frameborder=0></iframe>");
        },
        initDataRank: function (data) {
            if (typeof(AmCharts) === 'undefined' || $('#datarank').size() === 0) {
                return;
            }
            var colors = ['#FD0000', '#FE7E00', '#FEF001', '#01D85B', '#0188FE', '#8900FE', '#FF00E4', '#000000'];
            for (var i = 0; i < data.length; ++i) {
                data[i]['color'] = colors[i % colors.length]
            }

            var chart = AmCharts.makeChart("datarank", {
                "type": "serial",
                "categoryField": "category",
                "rotate": true,
                "startDuration": 1,
                "startEffect": "easeInSine",
                "fontSize": 12,
                "export": {
                    "enabled": true
                },
                "categoryAxis": {
                    "gridPosition": "start"
                },
                "trendLines": [],
                "graphs": [
                    {
                        "balloonText": "[[category]]: [[value]]%",
                        "colorField": "color",
                        "fillAlphas": 1,
                        "id": "AmGraph-1",
                        "labelOffset": 10,
                        "labelPosition": "right",
                        "labelText": "[[value]]%",
                        "lineThickness": 0,
                        "title": "graph 1",
                        "type": "column",
                        "valueField": "rate"
                    }
                ],
                "guides": [
                    {
                        "above": true,
                        "balloonColor": "#00B300",
                        "boldLabel": true,
                        "color": "#00B300",
                        "dashLength": 8,
                        "fillAlpha": 0,
                        "fillColor": "#00B300",
                        "fontSize": 12,
                        "id": "Guide-1",
                        "label": "35",
                        "lineAlpha": 0.9,
                        "lineColor": "#00B300",
                        "lineThickness": 3,
                        "tickLength": 0,
                        "value": 35
                    }
                ],
                "valueAxes": [
                    {
                        "id": "ValueAxis-1",
                        "stackType": "regular",
                        "title": ""
                    }
                ],
                "allLabels": [],
                "balloon": {},
                "titles": [
                    {
                        "id": "Title-1",
                        "size": 15,
                        "text": "产品兑奖率"
                    }
                ],
                "dataProvider": data
            });
        },
        initDataFormation: function (accepted, total) {
            if (typeof(AmCharts) === 'undefined' || $('#dataformation').size() === 0) {
                return;
            }

            var chart = AmCharts.makeChart("dataformation", {
                "type": "gauge",
                "startDuration": 5,
                "startEffect": "easeOutSine",
                "export": {
                    "enabled": true
                },
                "arrows": [
                    {
                        "id": "GaugeArrow-1",
                        "value": accepted / 10000
                    }
                ],
                "axes": [
                    {
                        "bottomText": accepted.toString() + "元",
                        "bottomTextColor": "#00CC00",
                        "bottomTextFontSize": 21,
                        "bottomTextYOffset": -20,
                        "endValue": total / 10000,
                        "id": "GaugeAxis-1",
                        "unit": " 万元",
                        "valueInterval": total / 100000,
                        "bands": [
                            {
                                "color": "#00CC00",
                                "endValue": total / 50000,
                                "id": "GaugeBand-1",
                                "startValue": 0
                            },
                            {
                                "color": "#ffac29",
                                "endValue": total / 20000,
                                "id": "GaugeBand-2",
                                "innerRadius": "96%",
                                "startValue": total / 50000
                            },
                            {
                                "color": "#ea3838",
                                "endValue": total / 10000,
                                "id": "GaugeBand-3",
                                "innerRadius": "94%",
                                "startValue": total / 20000
                            }
                        ]
                    }
                ],
                "allLabels": [],
                "balloon": {},
                "titles": [
                    {
                        "id": "Title-1",
                        "size": 15,
                        "text": "奖金池兑奖情况"
                    }
                ]
            });
        },
        init: function () {
            var that = this;
            var list = $('#dropdown_btn ul li a');
            if (list == null) {
                list = [];
            }
            var ids = [];
            for (var i = 0; i < list.length; ++i) {
                var item_id = list[i].id;
                ids.push((item_id.split('_'))[1]);
            }
            if (ids.length != 0) {
                that.refresh(ids[0])
            }

            $.ajax({
                type: 'GET',
                url: 's/accepted_rate',
                success: function (data) {
                    if (data['error_code'] == 0) {
                        that.initDataRank(data['data']);
                    }
                }
            });

            that.initSpiderBalance();
        },
        refresh: function (batch_id) {
            var that = this;
            $.ajax({
                type: 'GET',
                url: 's/scan_count/' + batch_id,
                success: function (data) {
                    if (data['error_code'] == 0) {
                        $('#total_scan').text(data['data']);
                        $('#dropdown_btn_title').text('生产批次' + batch_id.toString())
                    }
                }
            });

            $.ajax({
                type: 'GET',
                url: 's/code_count/' + batch_id,
                success: function (data) {
                    if (data['error_code'] == 0) {
                        $('#total_code').text(data['data']);
                    }
                }
            });

            $.ajax({
                type: 'GET',
                url: 's/accepted_and_award_amount/' + batch_id,
                success: function (data) {
                    if (data['error_code'] == 0) {
                        var accepted = data['data']['accepted'];
                        var total = data['data']['award'];
                        that.initDataFormation(accepted, total);
                        $('#total_accepted').text(accepted);
                    }
                }
            });

            $.ajax({
                type: 'GET',
                url: 's/daily_count/' + batch_id,
                success: function (data) {
                    if (data['error_code'] == 0) {
                        that.initDataTrend(data['data'])
                    }
                }
            });
        }
    };
}();


if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function () {
        dashboard.init(); // init metronic core components
        $('#dropdown_btn ul li a').each(function (index, item) {
            $(this).bind('click', function () {
                const bid = item.id.split('_')[1];
                dashboard.refresh(bid);
            })
        })
    });
}
