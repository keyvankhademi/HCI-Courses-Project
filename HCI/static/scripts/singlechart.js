
function random_number()
{
    return Math.floor((Math.random() * 143) + 66);
}

function get_colors(n)
{
    colors = []

    for(var i=0;i<n;i++)
    {
        colors.push('rgba(' + random_number() + ' ,' + random_number() + ' ,' + random_number() + ',1)');
    }
    console.log(colors)
    return colors;
}

function single_chart()
{
    //var colors = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850", '#d14641', '#d47b44', '#d6a646', '#d9d24a', '#4cdbb5']
    var colors = [];
    var d_labels = []
    var d_values = []
    var d_size = 60;
    var d_type = "";
    var m_chart = null;

    var terms_address = $('#terms_link').text();
    var sent_address = $('#sent_link').text();

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

    $('#b_sent_hist').click(function ()
    {

        $.ajax
            ({
                url: sent_address,

                success: function (data)
                {
                    d_title = data.title;
                    d_labels = data.labels;
                    d_values = data.values;
                    d_size = 20;
                    d_type = 'horizontalBar'
                    create_chart()

                    $('#size_input').val(d_size);
                }

            });
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
    });

    function create_chart()
    {
        colors = get_colors(d_size);

        if (m_chart != null) m_chart.destroy();
        m_chart = new Chart(document.getElementById("chart-content"), {
            type: d_type,
            data:
            {
                labels: d_labels.slice(0, d_size),
                datasets: [
                    {
                        label: 'amount',
                        backgroundColor: colors,
                        data: d_values.slice(0, d_size)
                    }
                ]
            },
            options:
            {
                legend: { display: false },
                scales: {
                    yAxes: [{
                        ticks:
                        {
                            suggestedMin: 0
                        }
                    }]
                }
            }
        });
    }


    $(document).on('click', '#b_piechart', function ()
    {
        d_type = 'pie';
        create_chart();
    });

    $(document).on('click', '#b_barchart', function ()
    {
        d_type = 'bar';
        create_chart('bar');
    });

    $('#size_input').on('input', function ()
    {
        d_size = this.value;
        create_chart();
    });
};
