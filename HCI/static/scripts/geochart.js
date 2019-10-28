$(document).ready(function ()
{

    var geo_data = []

    $.ajax
        ({
            url: '/charts/geodata/',
            success: function (data)
            {
                //geo_data = data['country density']
                geo_data = data
            }
        });

    google.charts.load('current', {
        'packages': ['geochart'],
        'mapsApiKey': 'AIzaSyC3hT-LFxgf1vgIigLyBJ5UF9RT8lnXA6c'
    });

    google.charts.setOnLoadCallback(drawRegionsMap);
    google.charts.setOnLoadCallback(drawCountriesMap);

    function drawRegionsMap()
    {
        var data = []
        data = google.visualization.arrayToDataTable((geo_data['region density']));

        var options =
        {
            region: '021',
            displayMode: 'markers',
            colorAxis:
            {
                minValue: 1,
                colors: ['#ff9d2e', '#3f5cff']
            }
        };

        var chart = new google.visualization.GeoChart(document.getElementById('region_density'));

        chart.draw(data, options);
    }

    function drawCountriesMap()
    {
        var data = []

        data = google.visualization.arrayToDataTable((geo_data['country density']));

        var options =
        {
            region: '021',
            colorAxis:
            {
                minValue: 1
            }

        };

        var chart = new google.visualization.GeoChart(document.getElementById('country_density'));

        chart.draw(data, options);
    }

});