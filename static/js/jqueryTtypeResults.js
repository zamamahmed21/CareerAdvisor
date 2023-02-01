$(document).ready(function(){

    // get Temperament type variable from local storage & insert into html
    let tType = sessionStorage.getItem("temperament_type");
    $("#t_type").text(tType); 

});