$(document).ready(function(){

    // get Temperament type variable from local storage & insert into html
    var t_type = localStorage.getItem("Temperament_type");
    $("#t_type").text(t_type); 

});