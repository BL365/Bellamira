A = function(hall) {
    var str = "/prices/" + document.getElementById('st_t').value + "/" + document.getElementById('end_t').value + "/" + hall + "/"
    jQuery.getJSON(
        str,
        function(json) {
                res = (json.result);
                if (res == true) {
                    document.getElementById('form0').submit();
                } else {
                    alert("Указанное время занято");
                }
    });
    return false;
}