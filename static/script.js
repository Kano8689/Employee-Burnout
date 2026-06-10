// 1. Speedometer (Gauge) Logic
function renderGauge(value) {
    const ctx = document.getElementById('burnoutGauge').getContext('2d');
    
    // Determine color based on value
    let color = '#10b981'; // Green
    if (value > 0.4) color = '#f59e0b'; // Yellow
    if (value > 0.7) color = '#ef4444'; // Red

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 1 - value], // Value vs Empty space
                backgroundColor: [color, '#e2e8f0'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            rotation: -90,         // Start at 9 o'clock (Left)
            circumference: 180,    // Half circle to 3 o'clock (Right)
            cutout: '75%',         // Thickness of the gauge
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}

// 2. Dashboard Impact Chart Logic
function renderImpactChart(impactData) {
    const ctx = document.getElementById('impactChart');
    if(!ctx) return;

    const labels = Object.keys(impactData).map(k => k.replace('_', ' '));
    const data = Object.values(impactData);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Impact Percentage (%)',
                data: data,
                backgroundColor: '#2563eb'
            }]
        },
        options: {
            indexAxis: 'y', // Horizontal bar chart
            scales: {
                x: { beginAtZero: true, max: 100 }
            }
        }
    });
}