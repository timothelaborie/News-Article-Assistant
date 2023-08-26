let server_url = "http://127.0.0.1:8000"

document.addEventListener('DOMContentLoaded', function () {
  console.log('popup.js loaded');

  $('#summarize').click(function () {
    console.log('clicked');
    let text = $('#original_text').val();
    let encoded_text = btoa(text);
    fetch(server_url + `/api/summary/${encoded_text}`, {
      method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
      alert(data.summary);
    })
    .catch(err => {
      alert("There was an error processing the request:", err);
    });
  });




}, false);