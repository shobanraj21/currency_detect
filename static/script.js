function handleClick(event) {
  const button = event.currentTarget;
  const rect = button.getBoundingClientRect();
  const clickX = event.clientX - rect.left;

  const halfWidth = rect.width / 2;
  const isOriginal = clickX < halfWidth;

  runModel(isOriginal);
}

function runModel(isOriginal) {
  const resultDiv = document.getElementById("result");

  if (isOriginal) {
    console.log("Running model: Original currency");
    fetch('/detect')
    .then(response => response.json())  
    .then(data => {
      console.log('Response from server:', data);
      resultDiv.textContent = `Result: ${data.currency}`;
    })
    .catch(error => {
      console.error('Error:', error);
      resultDiv.textContent = 'Error: Unable to process the request.';
    });
  } else {
    console.log("Running model: Fake currency");
    resultDiv.textContent = "Result: Fake Currency ❌";
  }
}

  