$(document).ready(function() {
    $("#leaderboard-tasks li").on("click", function(e) {
        var el = $(this);
        var task = el.data('task');

        if (!el.hasClass('active')) {
            el.siblings().removeClass('active');
            el.addClass('active');
        }

        maxRows = 4
        $.ajax({
            url: "leaderboard/" + task + "/time.html",
            cache: false
        }).done(function (html) {
            $("#leaderboard-time").html(html);
            $("#leaderboard-time tr:gt(" + maxRows + ")").hide();
        });

        $.ajax({
            url: "leaderboard/" + task + "/cost.html",
            cache: false
        }).done(function (html) {
            $("#leaderboard-cost").html(html);
            $("#leaderboard-cost tr:gt(" + maxRows + ")").hide();
        });

        $.ajax({
            url: "leaderboard/" + task + "/latency.html",
            cache: false
        }).done(function (html) {
            $("#leaderboard-latency").html(html);
            $("#leaderboard-latency tr:gt(" + maxRows + ")").hide();
        });

        $.ajax({
            url: "leaderboard/" + task + "/throughput.html",
            cache: false
        }).done(function (html) {
            $("#leaderboard-throughput").html(html);
            $("#leaderboard-throughput tr:gt(" + maxRows + ")").hide();
        });

        e.preventDefault();
    });

    $(document).on("click", ".leaderboard-toggle", function(e) {
        var el = $(this);
        var board = el.data('board');
        var action = el.text();
        var rows = $(board + ' tr:gt(4)');

        if (action == 'Expand') {
            rows.show();
            el.text('Collapse');
        } else if (action == 'Collapse') {
            rows.hide();
            el.text('Expand');
        }
        e.preventDefault();
    });

    $('#leaderboard-tasks li.active').click();
});
