$(document).ready(function()
{
    $('#d_main').children().hide();
    $('#d_single_graphs').show();

    $('#m_single').click(function()
    {
        $('#d_main').children().hide();
        $('#d_single_graphs').show();
    });

    $('#m_comp').click(function ()
    {
        $('#d_main').children().hide();
        $('#d_compare').show();
    });

    $('#m_geo').click(function ()
    {
        $('#d_main').children().hide();
        $('#d_geo_data').show();
    });

    $('#m_img').click(function ()
    {
        $('#d_main').children().hide();
        $('#d_images').show();
    });

});

