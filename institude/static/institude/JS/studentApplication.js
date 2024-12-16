

    document.querySelectorAll('input[type="radio"][value="rejected"]').forEach(function (radioBtn) {
    radioBtn.addEventListener('change', function () {
        var row = this.closest('tr').nextElementSibling; // Get the next sibling row
        if (row && row.classList.contains('rejection-row')) {
            row.style.display = this.checked ?'block' : 'none'; // Show/hide the rejection row
        }
    });
});

// Also hide the rejection row if the "approve" option is selected
document.querySelectorAll('input[type="radio"][value="approved"]').forEach(function (radioBtn) {
    radioBtn.addEventListener('change', function () {
        var row = this.closest('tr').nextElementSibling; // Get the next sibling row
        if (row && row.classList.contains('rejection-row')) {
            row.style.display = 'none'; // Hide the rejection row
        }
    });
});

// Add event listener to the close button
document.querySelectorAll('.close-btn').forEach(function (button) {
    button.addEventListener('click', function () {
        var row = this.closest('tr'); // Get the closest row containing the button
        var textArea = row.querySelector('.reject-reason'); // Find the text area within the row
        
        // Check if there's text inside the textarea
        if (textArea.value.trim() !== "") {
            row.style.display = 'none'; // Hide the row if there's text in the textarea
        } else {
            alert("Please enter a rejection reason before closing.");
        }
    });
});


/*
// Position the close button at the top right corner of its parent container
document.querySelectorAll('.close-btn').forEach(function (button) {
    button.style.position = 'absolute';
    button.style.top = '5px';
    button.style.right = '5px';
});

*/