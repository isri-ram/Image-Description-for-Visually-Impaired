// Get a reference to the button and output div
const processButton = document.getElementById('processImages');
const outputDiv = document.getElementById('output');

// Function to inject content_script.js into the current tab
function injectContentScript() {
    try {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
          const tab = tabs[0];
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: function () {
              // This code will be executed in the context of the current webpage
              const script = document.createElement('script');
              script.src = chrome.runtime.getURL('content_script.js');
              document.head.appendChild(script);
            },
          });
          outputDiv.textContent = 'Content script injected.';
        });
      } catch (error) {
        outputDiv.textContent = 'Error injecting content script: ' + error.message;
      }
}

// Add a click event listener to the button
processButton.addEventListener('click', injectContentScript);
