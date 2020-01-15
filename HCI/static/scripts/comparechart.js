function compare_chart()
{
    colours = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850", '#d14641', '#d47b44', '#d6a646', '#d9d24a', '#4cdbb5']
    d_all = {labels: [], values: []}
    d_cad = {labels: [], values: []}
    d_us = {labels: [], values: []}

    chart_l = null;
    chart_r = null;

    max_x_value = 140;

    function create_chart(data, id, size = 10)
    {

        return new Chart(document.getElementById(id),
            {
                type: 'horizontalBar',
                data:
                {
                    labels: data.labels.slice(0,size),
                    datasets: [
                        {
                            label: 'amount',
                            backgroundColor: colours,
                            data: data.values.slice(0,size)
                        }
                    ]
                },
                options:
                {
                    responsive: true,
                    legend: { display: false },
                    scales: {
                        xAxes: [{
                            ticks:
                            {
                                suggestedMin: 0,
                                suggestedMax: max_x_value
                            }
                        }]
                    }
                }
            });
    }

    function get_selected(value)
    {
        switch (String(value).trim())
        {
            case 'All':
                return d_all;
            case 'Canada':
                return d_cad;
            case 'USA':
                return d_us;
        }
    }

    function load_all()
    {
        return $.ajax
        ({
                url: $('#terms_link').text(),

                success: function (data)
                {
                    d_all.labels = data.labels;
                    d_all.values = data.values;
                    max_x_value = data.values[0];
                }
        });
    }

    function load_cad()
    {
        return $.ajax
        ({
            url: $('#ca_terms_link').text(),

            success: function (data)
            {
                d_cad.labels = data.labels;
                d_cad.values = data.values;
            }
        });
    }

    function load_us()
    {
        return $.ajax
            ({
                url: $('#us_terms_link').text(),

                success: function (data)
                {
                    d_us.labels = data.labels;
                    d_us.values = data.values;
                }
            });
    }

    $.when(load_all(), load_cad(), load_us()).done(function ()
    {
        var selected = $('#country_select_1 option:selected').text();
        var d_selected = get_selected(selected);
        chart_l = create_chart(d_selected,"cc1");

        var selected = $('#country_select_2 option:selected').text();
        var d_selected = get_selected(selected);
        chart_r = create_chart(d_selected,"cc2");
    });


    $('#country_select_1').change(function ()
    {
        chart_l.destroy()
        var selected = $('#country_select_1 option:selected').text();
        var d_selected = get_selected(selected);
        chart_l = create_chart(d_selected, "cc1");
    });

    $('#country_select_2').change(function ()
    {
        chart_r.destroy();
        selected = $('#country_select_2 option:selected').text();
        d_selected = get_selected(selected);
        chart_r = create_chart(d_selected, "cc2");
    });


};
