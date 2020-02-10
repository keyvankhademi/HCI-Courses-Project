function year_hist()
{
    colors = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850", '#d14641', '#d47b44', '#d6a646', '#d9d24a', '#4cdbb5']
    var years_address = $('#years_link').text();
    data = {labels: [], values: []}

    $.ajax
    ({
        url: years_address,

        success: function (response)
        {
            data.labels = response.labels;
            data.values = response.values;

            create_chart();
        }
    });

    function create_chart()
    {
        new Chart(document.getElementById('year_syllabus'),
            {
                type: 'bar',
                data:
                {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'amount',
                            backgroundColor: colors,
                            data: data.values
                        }
                    ]
                },
                options:
                {
                    legend: { display: false }
                }
            });
    }
};
