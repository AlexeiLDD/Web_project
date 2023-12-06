$(document).ready(function() {
    $(".anchor").click(function () {
        var elementClick = $(this).attr("href")
        var destination = $(elementClick).offset().top - $('.top_header').height();
        jQuery("html:not(:animated),body:not(:animated)").animate({scrollTop: destination}, 800);
        return false;
    });
})