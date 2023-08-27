let server_url = "http://127.0.0.1:8000"

document.addEventListener('DOMContentLoaded', function () {

  // $("#response").html("Nvidia, a technology giant, has reported record sales after its revenue more than doubled to above $13.5 billion in the quarter ending June. The company expects its sales to continue to soar in the current quarter and has plans to repurchase $25 billion of its stock. Its shares rose by over 6.5% in extended trading in New York, adding to the significant gains it has made this year. Nvidia expects its revenue for the quarter ending September to be around $16 billion, which is significantly higher than Wall Street expectations and a 170% increase compared to the same time last year.");


  function sendToServer(text, api){
    let encoded_text = btoa(text);
    fetch(server_url + `/api/${api}/${encoded_text}`, {
      method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
      $("#response").html(data.response);
    })
    .catch(err => {
      alert("There was an error processing the request:", err);
    });
  }

  $('#summarize').click(function () {
    let text = $('#original_text').val();
    sendToServer(text, "summary");
  });

  $('#extract').click(function () {
    let text = $('#original_text').val();
    sendToServer(text, "extract");
  })

  $('#generate').click(function () {
    let text = $('#original_text').val();
    sendToServer(text, "generate");
  })




}, false);