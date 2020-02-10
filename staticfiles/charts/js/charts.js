$(document).ready(function()
{
    $('#main_div').children().hide();
    $('#histograms_div').show();

    single_chart();
    compare_chart();

    $('#histograms_tab').click(function()
    {
        $('#main_div').children().hide();
        $('#histograms_div').show();
    });

    $('#metadata_tab').click(function ()
    {
        geo_chart();
        year_hist();

        $('#main_div').children().hide();
        $('#metadata_div').show();
    });
});
