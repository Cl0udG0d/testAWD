var ROOT_PATH = 'https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples';

// 折线图
var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option2;

$.get(ROOT_PATH + '/data/asset/data/life-expectancy-table.json', function(_rawData) {
    run(_rawData);
});

function run(_rawData) {

    // var countries = ['Australia', 'Canada', 'China', 'Cuba', 'Finland', 'France', 'Germany', 'Iceland', 'India', 'Japan', 'North Korea', 'South Korea', 'New Zealand', 'Norway', 'Poland', 'Russia', 'Turkey', 'United Kingdom', 'United States'];
    var countries = ['Finland', 'France', 'Germany', 'Iceland', 'Norway', 'Poland', 'Russia', 'United Kingdom'];
    var datasetWithFilters = [];
    var seriesList = [];
    echarts.util.each(countries, function(country) {
        var datasetId = 'dataset_' + country;
        datasetWithFilters.push({
            id: datasetId,
            fromDatasetId: 'dataset_raw',
            transform: {
                type: 'filter',
                config: {
                    and: [{
                        dimension: 'Year',
                        gte: 1950
                    }, {
                        dimension: 'Country',
                        '=': country
                    }]
                }
            }
        });
        seriesList.push({
            type: 'line',
            datasetId: datasetId,
            showSymbol: false,
            name: country,
            endLabel: {
                show: true,
                formatter: function(params) {
                    return params.value[3] + ': ' + params.value[0];
                }
            },
            labelLayout: {
                moveOverlap: 'shiftY'
            },
            emphasis: {
                focus: 'series'
            },
            encode: {
                x: 'Year',
                y: 'Income',
                label: ['Country', 'Income'],
                itemName: 'Year',
                tooltip: ['Income'],
            }
        });
    });

    option2 = {
        animationDuration: 10000,
        dataset: [{
            id: 'dataset_raw',
            source: _rawData
        }].concat(datasetWithFilters),
        title: {
            text: '前十队伍得分情况'
        },
        tooltip: {
            order: 'valueDesc',
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            nameLocation: 'middle'
        },
        yAxis: {
            name: '分数'
        },
        grid: {
            right: 140
        },
        series: seriesList
    };

    myChart.setOption(option2);

}

option2 && myChart.setOption(option2);

// 条形图
var chartDom = document.getElementById('main2');
var myChart2 = echarts.init(chartDom);
var option2;

var updateFrequency = 2000;
var dimension = 0;

var countryColors = { "Australia": "#00008b", "Canada": "#f00", "China": "#ffde00", "Cuba": "#002a8f", "Finland": "#003580", "France": "#ed2939", "Germany": "#000", "Iceland": "#003897", "India": "#f93", "Japan": "#bc002d", "North Korea": "#024fa2", "South Korea": "#000", "New Zealand": "#00247d", "Norway": "#ef2b2d", "Poland": "#dc143c", "Russia": "#d52b1e", "Turkey": "#e30a17", "United Kingdom": "#00247d", "United States": "#b22234" };

$.when(
    $.getJSON('https://cdn.jsdelivr.net/npm/emoji-flags@1.3.0/data.json'),
    $.getJSON(ROOT_PATH + '/data/asset/data/life-expectancy-table.json')
).done(function(res0, res1) {
    var flags = res0[0];
    var data = res1[0];
    var years = [];
    for (var i = 0; i < data.length; ++i) {
        if (years.length === 0 || years[years.length - 1] !== data[i][4]) {
            years.push(data[i][4]);
        }
    }

    function getFlag(countryName) {
        if (!countryName) {
            return '';
        }
        return (flags.find(function(item) {
            return item.name === countryName;
        }) || {}).emoji;
    }
    var startIndex = 10;
    var startYear = years[startIndex];

    var option2 = {
        grid: {
            top: 10,
            bottom: 30,
            left: 150,
            right: 80
        },
        xAxis: {
            max: 'dataMax',
            label: {
                formatter: function(n) {
                    return Math.round(n);
                }
            }
        },
        dataset: {
            source: data.slice(1).filter(function(d) {
                return d[4] === startYear;
            })
        },
        yAxis: {
            type: 'category',
            inverse: true,
            max: 10,
            axisLabel: {
                show: true,
                textStyle: {
                    fontSize: 14
                },
                formatter: function(value) {
                    return value + '{flag|' + getFlag(value) + '}';
                },
                rich: {
                    flag: {
                        fontSize: 25,
                        padding: 5
                    }
                }
            },
            animationDuration: 300,
            animationDurationUpdate: 300
        },
        series: [{
            realtimeSort: true,
            seriesLayoutBy: 'column',
            type: 'bar',
            itemStyle: {
                color: function(param) {
                    return countryColors[param.value[3]] || '#5470c6';
                }
            },
            encode: {
                x: dimension,
                y: 3
            },
            label: {
                show: true,
                precision: 1,
                position: 'right',
                valueAnimation: true,
                fontFamily: 'monospace'
            }
        }],
        // Disable init animation.
        animationDuration: 0,
        animationDurationUpdate: updateFrequency,
        animationEasing: 'linear',
        animationEasingUpdate: 'linear',
        graphic: {
            elements: [{
                type: 'text',
                right: 160,
                bottom: 60,
                style: {
                    text: startYear,
                    font: 'bolder 80px monospace',
                    fill: 'rgba(100, 100, 100, 0.25)'
                },
                z: 100
            }]
        }
    };

    // console.log(option2);
    myChart2.setOption(option2);

    for (var i = startIndex; i < years.length - 1; ++i) {
        (function(i) {
            setTimeout(function() {
                updateYear(years[i + 1]);
            }, (i - startIndex) * updateFrequency);
        })(i);
    }

    function updateYear(year) {
        var source = data.slice(1).filter(function(d) {
            return d[4] === year;
        });
        option2.series[0].data = source;
        option2.graphic.elements[0].style.text = year;
        myChart2.setOption(option2);
    }
})

option2 && myChart2.setOption(option2);