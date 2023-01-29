$(document).ready(function(){

    // get personality type variable from local storage & insert in html
    var p_type = localStorage.getItem("personality_type");
    $("#p_type").text(p_type);

});