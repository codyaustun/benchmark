$(document).ready(function() {
    $("#leaderboard-buttons li").on("click", function(e) {
        var el = $(this);
        var board = el.data('board')

        if (!el.hasClass('active')) {
            el.siblings().removeClass('active')
            el.addClass('active')
        }
        console.log("button clicked!" + board)

        $.ajax({
            url: "leaderboard/" + board + ".html",
            cache: false
        }).done(function (html) {
            $("#leaderboard").html(html);
        });

        e.preventDefault();
    });

    $('#leaderboard-buttons li.active').click();
});
