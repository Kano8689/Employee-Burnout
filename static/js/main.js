document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Package the HTML form inputs automatically
    const formData = new FormData(this);

    // Send data to your Flask backend route securely
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Read the decimal value (0 to 1) sent back by Python
            updateUI(data.prediction);
        } else {
            console.error('Prediction failed:', data.error);
        }
    })
    .catch(error => {
        console.error('Error connecting to backend:', error);
    });
});

function updateUI(score) {
    const needle = document.getElementById('gaugeNeedle');
    const statusText = document.getElementById('resultStatus');
    const valueText = document.getElementById('resultValue'); // <-- Grab the new value element
    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');

    // Remove old state styling classes from status and value text
    statusText.classList.remove('text-muted', 'text-low', 'text-medium', 'text-high');
    valueText.classList.remove('text-muted', 'text-low', 'text-medium', 'text-high');
    alertBox.classList.remove('hidden', 'low-alert', 'medium-alert', 'high-alert');

    // Update the inner text to show the exact value rounded to 2 decimal places
    valueText.innerText = score.toFixed(2);

    // Convert score from range 0.0 - 1.0 to rotation degrees (-65deg to 65deg)
    const degrees = -65 + (score * 130);
    needle.style.transform = `rotate(${degrees}deg)`;

    // Render corresponding labels and colors based on metrics
    if (score <= 0.30) {
        statusText.innerText = "Low Burnout";
        statusText.classList.add('text-low');
        valueText.classList.add('text-low'); // Color the number green
        
        alertMessage.innerHTML = `<strong>This employee is well-managed.</strong><br>Keep up the current work-life structural conditions.`;
        alertBox.classList.add('low-alert');
    } 
    else if (score <= 0.60) {
        statusText.innerText = "Medium Burnout";
        statusText.classList.add('text-medium');
        valueText.classList.add('text-medium'); // Color the number orange
        
        alertMessage.innerHTML = `<strong>Signs of moderate strain detected.</strong><br>Monitor task loads and offer regular breaks.`;
        alertBox.classList.add('medium-alert');
    } 
    else {
        statusText.innerText = "High Burnout";
        statusText.classList.add('text-high');
        valueText.classList.add('text-high'); // Color the number red
        
        alertMessage.innerHTML = `<strong>This employee is likely experiencing high burnout.</strong><br>Consider taking necessary actions to improve well-being.`;
        alertBox.classList.add('high-alert');
    }
}