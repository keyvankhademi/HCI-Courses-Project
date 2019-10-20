$(document).ready(function()
{
    //////////////////////////////////////////////
    var g_data = [];
    
    $.ajax
        ({
            url: 'googletest',
            success: function (data)
            {
                g_data = data.data
            }
        });


    google.charts.load('current', { 'packages': ['corechart', 'controls'] });
    google.charts.setOnLoadCallback(draw_chart);

    function draw_chart()
    {
        var data = google.visualization.arrayToDataTable(g_data);

        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashboard_div'));

        // Create a range slider, passing some options
        var donutRangeSlider = new google.visualization.ControlWrapper({
            'controlType': 'NumberRangeFilter',
            'containerId': 'filter_div',
            'options': {
                'filterColumnLabel': 'year',
                'vAxis':
                { 'format': 'none' }
            }
        });

        // Create a pie chart, passing some options
        var barChart = new google.visualization.ChartWrapper({
            'chartType': 'Histogram',
            'containerId': 'chart_div',
            'options': {
                'width': 900,
                'height': 400,
                'legend': 'right',
                'colors': ['#aad2ff','Yellow', '#aad2ff'],
                'histogram':
                {
                    'bucketSize':1,
                    
                },
                
            },
            
        });

        dashboard.bind(donutRangeSlider, barChart);
        dashboard.draw(data);
    }


    /////////////////////////////////////////////////////////

    var d_labels = []
    var d_values = []
    var d_title = "";
    var d_size = 60;
    var d_type ="";
    var m_chart = null;

    var terms_address = $('#terms_link').text();
    var years_address = $('#years_link').text();

    $('#b_year_hist').click(function ()
    {
        $.ajax
            ({
                url: years_address,

                success: function (data)
                {
                    d_title = data.title;
                    d_labels = data.labels;
                    d_values = data.values;
                    d_size = d_labels.length;
                    d_type = 'bar'
                    create_chart()

                    $('#size_input').val(d_size);
                }

            });

        $(b_secondary).show();
    });

    $('#b_terms_hist').click(function ()
    {
        $.ajax
            ({
                url: terms_address,

                success: function (data)
                {
                    d_labels = data.labels;
                    d_values = data.values;
                    d_size = 50;
                    d_type = 'bar'

                    create_chart()
                    $('#size_input').val(d_size);
                }

            });
        $(b_secondary).show();

    });

    function create_chart()
    {
        if(m_chart != null)m_chart.destroy();
        m_chart = new Chart(document.getElementById("chart-content"), {
            type: d_type,
            data: {
                labels: d_labels.slice(0,d_size),
                datasets: [
                    {
                        label: 'amount',
                        backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                        data: d_values.slice(0, d_size)
                    }
                ]
            },
            options: {
                legend: { display: false },
                title: {
                    display: true,
                    text: d_title
                }
            }
        });
    }
    
    $(document).on('click','#b_piechart',function()
    {
        d_type = 'pie';
        create_chart();
    });

    $(document).on('click', '#b_barchart', function ()
    {
        d_type = 'bar';
        create_chart('bar');
    });
    
    $('#size_input').on('input',function()
    {
        d_size = this.value;
        create_chart();
    })

});

