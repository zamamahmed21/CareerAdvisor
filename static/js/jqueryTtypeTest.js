$(document).ready(function(){

    var section_idx =0

    var answers_map = new Map()

    let qa_data = $.getJSON({
        url: 'static/TemperamentQA.json',
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
    

    delete temp_map;
    delete qa_data;

    [a,b]=data_map.keys();
    var data_keys=[a,b]

    appendText()


    function appendText() {

        $("#TQA").append('<div>');
        $("#TQA div:first").append('<ol>');
        for (const x of data_map.get(data_keys[section_idx])) {

            first_letter = data_keys[section_idx].slice(0,1)
            second_letter = data_keys[section_idx].slice(-1)
            // in values, small letter equals to agree/disagree, captial letter equals to strongly agree/disagree
            $("#TQA ol:first").append(`<li> ${ x[0] } <br>`);
            $("#TQA li:last-child").append(`<input type='radio' name="${ x[0] }" value='${first_letter}'>&nbsp; ${ x[1][0] }`);
            $("#TQA li:last-child").append('<br>');
            $("#TQA li:last-child").append(`<input type='radio' name="${ x[0] }" value='${first_letter.toLowerCase()}'>&nbsp; ${ x[1][1] }`);
            $("#TQA li:last-child").append('<br>');
            $("#TQA li:last-child").append(`<input type='radio' name="${ x[0] }" value='${second_letter.toLowerCase()}'>&nbsp; ${ x[1][2] }`);
            $("#TQA li:last-child").append('<br>');
            $("#TQA li:last-child").append(`<input type='radio' name="${ x[0] }" value='${second_letter}'>&nbsp; ${ x[1][3] }`);
            $("#TQA ol:first").append('<br></li>');
        }
        $("#TQA").append('</ol>');
        $("#TQA").append('</div>');

    }

    function submitBtnVisibility(){

        if (section_idx==1){
            $("#next_btn").attr("hidden",true);
            $("#submit_btn").removeAttr("hidden");
        }
        else{
            $("#submit_btn").attr("hidden",true);
            $("#next_btn").removeAttr("hidden");       
        }
    }

    function storeAnswers(){
        let values = []

        for (const x of data_map.get(data_keys[section_idx])) { 
            
            values.push($(`input[name="${ x[0] }"]:checked`).val());  
        }

        //if (values.includes(undefined)){return}
        answers_map.set(data_keys[section_idx], values)
    }


    $("#next_btn").click(function(){
    // store answers of the selected points
   storeAnswers();
    // clear question/answer div
    $("#TQA").empty();
    // add question/answers
    section_idx = section_idx + 1
    appendText();
    submitBtnVisibility();
});

$("#prev_btn").click(function(){
    // exit function if section index is 0
    if (section_idx == 0){return}
    // clear question/answer div
    $("#TQA").empty();
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
    console.log(json)
    // send POST request to the URL where calculations will be carried out
    $.ajax({ 
        url: "/TemperamentTypeResult", 
        type: 'POST', 
        async: false,
        data: json,
        contentType: "application/json",
        success: function(response){ 
            // set variable's value within local storage
            sessionStorage.setItem("temperament_type", response);
            // goto this page
            window.location.href = "/TemperamentType/Results";
        } 
    });
});









    







})