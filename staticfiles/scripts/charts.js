$(document).ready(function()
{
    $('#main_div').children().hide();
    $('#histograms_div').show();

    $('#histograms_tab').click(function()
    {
        $('#main_div').children().hide();
        $('#histograms_div').show();
    });

    $('#metadata_tab').click(function ()
    {
        $('#main_div').children().hide();
        $('#metadata_div').show();
    });
});

