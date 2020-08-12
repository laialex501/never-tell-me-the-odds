$('#params').submit(function(event) {
    event.preventDefault();
    const post_url = '/estimate';
    const request_method = 'POST';

    // Acquire query parameters
    var ability = $('#a').val();
    var proficiency = $('#p').val();
    var difficulty = $('#d').val();
    var challenge = $('#c').val();
    var boost = $('#b').val();
    var setback = $('#s').val();
    var query = $('#q').val();
    var params = JSON.stringify({"ability": ability, "proficiency": proficiency, "difficulty": difficulty, "challenge": challenge, "boost": boost, "setback": setback, "query": query});

    $.ajax({
        url : post_url,
        type: request_method,
        contentType: "application/json",
        data: params,
        dataType: "json"
    }).done(function(data) {
        $('#output').text(`Probability of ${data.query_str} is: ${data.estimate}`)
    })
})
