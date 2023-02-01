$(document).ready(function(){

    // get personality type variable from local storage & insert into html
    let p_type = sessionStorage.getItem("personality_type");
    $("#p_type").text(p_type); 

});