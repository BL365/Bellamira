
var str1 = document.getElementById('st_t').value
var str2 = document.getElementById('end_t').value
var str = str1 + "/" + str2;
    A = function() {
        jQuery.getJSON(
        "/prices/str/$hall.id/",
        function(json) {
                return (json.result);
        });
        return (json.result);
    }