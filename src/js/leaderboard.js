$(document).ready(function() {
    $("#leaderboard-metrics li").on("click", function(e) {
        var el = $(this);
        var metric = el.data('metric')
        var task = $('#leaderboard-tasks li.active').data('task')

        if (!el.hasClass('active')) {
            el.siblings().removeClass('active')
            el.addClass('active')
        }

        $.ajax({
            url: "leaderboard/" + task + "/" + metric + ".html",
            cache: false
        }).done(function (html) {
            $("#leaderboard").html(html);
        });

        e.preventDefault();
    });

    $("#leaderboard-tasks li").on("click", function(e) {
        var el = $(this);
        var task = el.data('task')
        var metric = $('#leaderboard-metrics li.active').data('metric')

        if (!el.hasClass('active')) {
            el.siblings().removeClass('active')
            el.addClass('active')
        }

        $.ajax({
            url: "leaderboard/" + task + "/" + metric + ".html",
            cache: false
        }).done(function (html) {
            $("#leaderboard").html(html);
        });

        e.preventDefault();
    });

    $('#leaderboard-metrics li.active').click();
});
