$(document).ready(function()
{

    var d_labels = []
    var d_values = []
    var d_title = "";
    var d_size = 60;
    var d_type ="";
    var m_chart = null;

    $('#b_year_hist').click(function ()
    {
        $.ajax
            ({
                url: '/charts/years/frequency/',

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

        $(b_secondary).html('<button id="b_piechart" class="btn btn-secondary">pie chart</button>  <button id="b_barchart" class="btn btn-secondary">bar chart</button>');
    });

    $('#b_terms_hist').click(function ()
    {
        $.ajax
            ({
                url: '/charts/terms/frequency/',

                success: function (data)
                {
                    d_labels = data.labels;
                    d_values = data.values;
                    d_size = 50;
                    d_type = 'bar'
                    console.log(d_values);

                    create_chart()
                    $('#size_input').val(d_size);
                }

            });
        $(b_secondary).html('<button id="b_piechart" class="btn btn-secondary">pie chart</button>   <button id="b_barchart" class="btn btn-secondary">bar chart</button>');

    });

    function create_chart()
    {
        if(m_chart != null)m_chart.destroy();
        m_chart = new Chart(document.getElementById("bar-chart"), {
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
        console.log(1);
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

