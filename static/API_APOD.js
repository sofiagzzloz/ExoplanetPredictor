var req = new XMLHttpRequest();
var url = "https://api.nasa.gov/planetary/apod?api_key=";
var api_key = "mf7bn8QWV4WeYueyvoHsCphMAYhZIYpZda69Blgp";

req.open("GET", url + api_key);
req.onreadystatechange = function () {
    if (req.readyState === XMLHttpRequest.DONE) {
        if (req.status === 200) {
            var response = JSON.parse(req.responseText);
            document.getElementById("title").textContent = response.title;
            document.getElementById("date").textContent = response.date;
            document.getElementById("pic").src = response.hdurl;
            document.getElementById("explanation").textContent = response.explanation;
        } else {
            console.error('API request failed with status: ' + req.status);
            // Handle failures: display a default message or image
        }
    }
};
req.send();

