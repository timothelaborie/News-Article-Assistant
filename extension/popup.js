let server_url = "http://127.0.0.1:8000"

document.addEventListener('DOMContentLoaded', function () {


  function sendToServer(text, api, cb){
    let encoded_text = btoa(text);
    fetch(server_url + `/api/${api}/${encoded_text}`, {
      method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
      //$("#response").html(data.response);
      cb(data);
    })
    .catch(err => {
      alert("There was an error processing the request:", err);
    });
  }

  $('#summarize').click(function () {
    let text = $('#original_text').val();
    $("#textresponse").show();
    sendToServer(text, "summary", function(data){
      $("#response").html(data.response);
      $("#textresponse h2").text("Summary");
    });
    
  });

  $('#extract').click(function () {
    let text = $('#original_text').val();
    $("#textresponse").show();
    sendToServer(text, "extract", function(data){
      $("#response").html(data.response);
      $("#textresponse h2").text("Extracted Arguments");
    });
    
  })

  $('#generate_prompt').click(function () {
    let text = $('#original_text').val();
    sendToServer(text, "generate_prompt", function(data){
      $("#original_text").val(data.response);
    });
  })

  $('#generate_image').click(function () {
    let text = $('#original_text').val();
    $("#imgresponse").show();
    sendToServer(text, "generate_image", function(data){
      console.log(data.response);
      $("#response_img").attr("src", data.response);
      $("#imgresponse h2").text("Image");
    });
  })




}, false);