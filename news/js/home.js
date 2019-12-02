var last_query = "";
var page = 0;

function make_post(url, title, author, img_src, description, date) {
    return $(`
    <a class="item" href="` + url + `">
        <h3>` + title + `</h3>
        <h4>` + author + `</h4>
        <p>` + date + `</p>
        <img src="` + img_src + `">
        <p>` + description +`</p>
        <hr>
    </a>
    `)
}

function date_time_string(date) {
    var date = (new Date(date));
    return date.toDateString() + " at " + date.toTimeString();
}

function populate(data, sort){
    $("#results").html("");

    if($("#sorted").is(':checked')) {
        console.log("sort");
        data.articles.sort((a, b) => {
            (new Date(a.publishedAt)) - (new Date(b.publishedAt))
        });
    }

    console.log(data);

    data.articles.forEach(article => {
        $("#results").append($(make_post(
            article.url,
            article.title,
            article.author,
            article.urlToImage,
            article.description,
            date_time_string(article.publishedAt)
        )))
    });

    $("#results_title")[0].scrollIntoView();
}

$(document).ready(function(){
    $.getJSON("/api/get_news").then(populate);

    $("form").submit(() => {
        var query = $("#search_query").val();
        last_query = query;
        page = 0;
        $.getJSON("/api/get_news?q=" + query).then(populate);
        return false;
    })

    $("#prev").click(() => {
        page -= 1;
        if(last_query){
            $.getJSON("/api/get_news?q=" + query + "&page=" + page).then(populate);
        } else {
            $.getJSON("/api/get_news?page=" + page).then(populate);
        }
    })

    $("#next").click(() => {
        page += 1;
        if(last_query){
            $.getJSON("/api/get_news?q=" + query + "&page=" + page).then(populate);
        } else {
            $.getJSON("/api/get_news?page=" + page).then(populate);
        }
    })
})