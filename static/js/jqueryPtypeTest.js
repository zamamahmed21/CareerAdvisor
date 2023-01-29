$(document).ready(function(){

    // section index that increases/decreases upon clicking 'Next'/'Previous' to switch sections e.g. EI,SN,etc
    var section_idx = 0

    // a Map to store values of sections
    var answers_map = new Map()


    // get personality question/anwers' data from JSON file
    let qa_data = $.getJSON({
        url: 'static/QA.json',
        type: 'GET',
        async: false,
        success: function (data) {
            // console.log(data)
            return data;
        },
        contentType: 'application/json; charset=utf-8'
    });


    // access the Q/A data with responseText & create a Map containing pairs of section-type(key) & QA(values)
    var data_map = new Map(Object.entries(JSON.parse(qa_data.responseText)));
    // iterate over the map & create maps containing pairs of question(key) & answers(value)
    temp_map = data_map;
    for (const x of data_map.entries()) {
        temp_map.set(x[0],new Map(Object.entries(x[1])));
      }
    data_map = temp_map;

    // delete variables to free up memory
    delete temp_map;
    delete qa_data;

    // create a dictionary of keys
    [a,b,c,d,e] = data_map.keys();
    var data_keys = [a,b,c,d,e]

    appendText()


    // append text in question/answers div
    function appendText() {

        $("#QA").append('<div>');
        $("#QA div:first").append('<ol>');
        for (const x of data_map.get(data_keys[section_idx])) {
            // x[0] is question
            // x[1] has answers
            // slice(0,1) element of 'EI' means getting 'E'..
            $("#QA ol:first").append(`<li> ${ x[0] } <br>`);
            $("#QA li:last-child").append(`<input type='radio' name='${ x[0] }' value=${data_keys[section_idx].slice(0,1)}>&nbsp; ${ x[1][0] }`);
            $("#QA li:last-child").append('<br>');
            $("#QA li:last-child").append(`<input type='radio' name='${ x[0] }' value=${data_keys[section_idx].slice(-1)}>&nbsp; ${ x[1][1] }`);
            $("#QA ol:first").append('<br></li>');
        }
        $("#QA").append('</ol>');
        $("#QA").append('</div>');

    }

    // set visibility as hidden if no. of sections are equal to 3 or do otherwise
    function submitBtnVisibility(){

        if (section_idx==3){
            $("#next_btn").attr("hidden",true);
            $("#submit_btn").removeAttr("hidden");
        }
        else{
            $("#submit_btn").attr("hidden",true);
            $("#next_btn").removeAttr("hidden");       
        }
    }

    // store answers in a map
    function storeAnswers(){
        let values = []

        for (const x of data_map.get(data_keys[section_idx])) {
            values.push($(`input[name='${ x[0] }']:checked`).val());   
        }

        // if (values.includes(undefined)){return}

        answers_map.set(data_keys[section_idx], values)
    }


$("#next_btn").click(function(){
    // store answers of the selected points
    storeAnswers();
    // clear question/answer div
    $("#QA").empty();
    // add question/answers
    section_idx = section_idx + 1
    appendText();
    submitBtnVisibility();
});

$("#prev_btn").click(function(){
    // exit function if section index is 0
    if (section_idx == 0){return}
    // clear question/answer div
    $("#QA").empty();
    // add question/answers
    section_idx = section_idx - 1
    appendText();
    submitBtnVisibility();
});


$("#submit_btn").click(function(){
    
    // store answers of the selected points
    storeAnswers();
    
    // create a json from Map to send to server
    json = [];
    for (const map of answers_map.entries()) {
        json.push(map);
      }
    json = JSON.stringify(Object.fromEntries(json))
    
    // send POST request to the URL where calculations will be carried out
    $.ajax({ 
        url: "/PersonalityTypeResult", 
        type: 'POST', 
        async: false,
        data: json,
        contentType: "application/json",
        success: function(response){ 
            // set variable's value to be able to recieve it from within local storage through jquery
            localStorage.setItem("personality_type", response);
            // goto this page
            window.location.href = "/PersonalityType/Results";
        } 
    });
});


});
