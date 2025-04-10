frappe.ready(function() {
    document.getElementById('downloadBtn').addEventListener('click', function() {
        var mobileNumber = document.getElementById('mobileNumber').value;
        var resultDiv = document.getElementById('result');

        if (!mobileNumber || mobileNumber.length !== 10 || isNaN(mobileNumber)) {
            resultDiv.textContent = "Please enter a valid 10-digit mobile number.";
            resultDiv.className = 'result error'; // Set class for error styling
            resultDiv.style.display = 'block'; // Show the result div
            return; // Stop further execution
        }

        // Show loading state (optional - you can add a spinner or message)
        resultDiv.textContent = "Processing, please wait...";
        resultDiv.className = 'result'; // Reset class
        resultDiv.style.display = 'block';

        frappe.call({
            method: "your_app.your_module.download_result_by_mobile_no", // **IMPORTANT: Replace this**
            args: {
                mobile_no: mobileNumber
            },
            callback: function(r) {
                if (r.message.status === true) {
                    // Redirect to S3 URL
                    window.location.href = r.message.s3_presigned_url;
                } else {
                    // Display error message from backend
                    resultDiv.textContent = r.message.message;
                    resultDiv.className = 'result error'; // Set class for error styling
                    resultDiv.style.display = 'block';
                }
            },
            error_callback: function(error) {
                // Handle any errors during frappe.call
                console.error("Error calling function:", error);
                resultDiv.textContent = "Something went wrong. Please try again later.";
                resultDiv.className = 'result error'; // Set class for error styling
                resultDiv.style.display = 'block';
            }
        });
    });
});