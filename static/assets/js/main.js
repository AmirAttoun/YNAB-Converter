function startRedirectCountdown() {
    let countdownElement = document.getElementById('countdown');
    let countdownTime = 5; // seconds

    const intervalId = setInterval(() => {
        countdownTime--;
        countdownElement.innerText = countdownTime;

        if (countdownTime <= 0) {
            clearInterval(intervalId);
            window.location.href = "/"; // Redirect to the home page
        }
    }, 1000);
}

function setupDownloadAndRedirect() {
        const downloadButton = document.getElementById('submit');
        if (downloadButton) {
            downloadButton.addEventListener('click', function() {
                // Redirect after a short delay to ensure download dialog appears
                setTimeout(function() {
                    window.location.href = '/thankyou';
                }, 1000); // Delay may need adjustment based on actual download start
            });
        }
 
}
