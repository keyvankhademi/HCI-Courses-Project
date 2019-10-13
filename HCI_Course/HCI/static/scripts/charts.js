$(document).ready(function()
{

    d_labels = []
    d_values = []

    $('#b_year_hist').click(function ()
    {
        $.ajax
            ({
                url: '/charts/years/frequency/',

                success: function (data)
                {
                    d_labels = data.labels;
                    d_values = data.values;

                    console.log(d_values);

                    create_bar_chart(l = 'amount', t='syllabus years histogram' )
                }

            });


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

                    console.log(d_values);

                    create_bar_chart(l = 'amount', t = 'terms histogram')
                }

            });


    });

    function create_bar_chart(label,title)
    {
        new Chart(document.getElementById("bar-chart"), {
            type: 'bar',
            data: {
                labels: d_labels,
                datasets: [
                    {
                        label: l,
                        backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                        data: d_values
                    }
                ]
            },
            options: {
                legend: { display: false },
                title: {
                    display: true,
                    text: t
                }
            }
        });
    }
    

    
});

