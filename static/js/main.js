document.getElementById('predictionForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        if (!data.success) {
            console.error("Prediction failed:", data.error);
            return;
        }

        updateUI(
            data.score,
            data.level,
            data.recommendation,
            data.importance
        );
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


function updateUI(score, level, recommendation, importance) {

    const needle = document.getElementById('gaugeNeedle');
    const statusText = document.getElementById('resultStatus');
    const valueText = document.getElementById('resultValue');

    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');

    statusText.classList.remove(
        'text-muted',
        'text-low',
        'text-medium',
        'text-high'
    );

    valueText.classList.remove(
        'text-muted',
        'text-low',
        'text-medium',
        'text-high'
    );

    alertBox.classList.remove(
        'hidden',
        'low-alert',
        'medium-alert',
        'high-alert'
    );

    // Burnout Percentage
    const percentage = (score * 100).toFixed(1);

    valueText.innerText = `${percentage}%`;
    statusText.innerText = level;

    // Gauge rotation
    const degrees = -65 + (score * 130);
    needle.style.transform = `rotate(${degrees}deg)`;

    // Alert message
    alertMessage.innerHTML = recommendation;

    if (score <= 0.30) {

        statusText.classList.add('text-low');
        valueText.classList.add('text-low');
        alertBox.classList.add('low-alert');

    }
    else if (score <= 0.60) {

        statusText.classList.add('text-medium');
        valueText.classList.add('text-medium');
        alertBox.classList.add('medium-alert');

    }
    else {

        statusText.classList.add('text-high');
        valueText.classList.add('text-high');
        alertBox.classList.add('high-alert');

    }

    // Feature Importance Section
    const impactContainer = document.getElementById("featureImpact");

    if (impactContainer) {

        impactContainer.innerHTML = "";

        Object.entries(importance)
            .sort((a, b) => b[1] - a[1])
            .forEach(([feature, value]) => {

                impactContainer.innerHTML += `
                    <div class="impact-row">
                        <span>${feature.replaceAll('_', ' ')}</span>
                        <strong>${value.toFixed(2)}%</strong>
                    </div>
                `;
            });
    }

    console.log("Burnout Score:", score);
    console.log("Feature Importance:", importance);
}