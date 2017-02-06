A = function(hall) {
    var str = "/prices/" + document.getElementById('st_t').value + "/" + document.getElementById('end_t').value + "/" + hall + "/"
    jQuery.getJSON(
        str,
        function(json) {
                return (json.result);
    });
    return (json.result);
}