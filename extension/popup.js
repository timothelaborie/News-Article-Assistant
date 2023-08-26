let server_url = "http://127.0.0.1:8000"

document.addEventListener('DOMContentLoaded', function () {
  console.log('popup.js loaded');


  $('#summarize').click(function () {
    console.log('clicked');
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var activeTab = tabs[0];
      chrome.tabs.sendMessage(activeTab.id, {"message": "get_html"}, function(response) {
        // Here, the 'response' will be the HTML content of the page
        processResponse(response);
      });
    });

  });

  function processResponse(response) {
    console.log(response);
    // response = response.substr(0, 200);
    let encoded_response = btoa(response);
    fetch(server_url + `/api/summary/${encoded_response}`, {
      method: 'POST',
      headers: {
          'ngrok-skip-browser-warning': 'true'
          // 'Origin': window.location.origin,
      }
    })
    .then(response => response.json())
    .then(data => {
      alert(data.summary);
      
    })
    .catch(err => {
      alert("There was an error processing the request:", err);
    });
  }


}, false);