document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const resultCard = document.getElementById('resultCard');
    const errorCard = document.getElementById('errorCard');
    const resultContent = document.getElementById('resultContent');
    const errorContent = document.getElementById('errorContent');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Hide previous results
        resultCard.style.display = 'none';
        errorCard.style.display = 'none';

        // Get form data
        const formData = {
            feature1: parseFloat(document.getElementById('feature1').value),
            feature2: parseFloat(document.getElementById('feature2').value),
            feature3: parseFloat(document.getElementById('feature3').value)
        };

        // Show loading state
        resultCard.style.display = 'block';
        resultContent.innerHTML = '<div class="loading"><div class="spinner"></div><p>Processing prediction...</p></div>';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                // Display success result
                resultCard.style.display = 'block';
                resultContent.innerHTML = `
                    <div class="result-item">
                        <strong>Prediction:</strong> ${data.prediction}
                    </div>
                    <div class="result-item">
                        <strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%
                    </div>
                `;
            } else {
                // Display error
                errorCard.style.display = 'block';
                errorContent.textContent = data.error || 'An error occurred during prediction';
            }
        } catch (error) {
            // Display network error
            errorCard.style.display = 'block';
            errorContent.textContent = `Network error: ${error.message}`;
        }
    });
});
