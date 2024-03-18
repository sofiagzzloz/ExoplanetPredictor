document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('predictionForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        // Gather the form data
        const formData = new FormData(e.target);
        const formProps = Object.fromEntries(formData);

        // Prepare the data to be sent in the POST request
        let requestData = { features: [] };
        for (let key in formProps) {
            requestData.features.push(parseFloat(formProps[key]));
        }

        console.log('Data to be sent to the model:', requestData);

        // Make the POST request to the Flask API
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            // Display the prediction result
            document.getElementById('predictionResult').textContent = 
                'Prediction: ' + (data.prediction === 1 ? 'Exoplanet' : 'Not an Exoplanet');
            console.log('Prediction response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('predictionResult').textContent = 
                'An error occurred. Please try again.';
        });
    });
});
