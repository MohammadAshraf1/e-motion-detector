let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                // Show valid response
                document.getElementById("system_response").innerHTML = xhttp.responseText;
            } else if (this.status == 400) {
                // Show error message from server (e.g. blank input)
                document.getElementById("system_response").innerHTML = "Invalid text! Please try again!";
            }
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze), true);
    xhttp.send();
};
