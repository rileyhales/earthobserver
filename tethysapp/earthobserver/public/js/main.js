$("#model").change(function () {
    let model = $(this).val();
    if (model === 'gldas') {
        $("#gldas").css({'display':'initial'});
        $("#gfs").css({'display':'none'});
    } else if (model === 'gfs') {
        $("#gldas").css({'display':'none'});
        $("#gfs").css({'display':'initial'});
    }
});