// scripts.js
  document.addEventListener('DOMContentLoaded', function() {
        const passwordHidden = document.getElementById('pwd');
        const passwordVisible = document.getElementById('pwd-reveal');
        let isPasswordHidden = true; // Initial state

        // Function to toggle password visibility
        function togglePasswordVisibility() {
            console.log(pwd.value,isPasswordHidden);
            if (isPasswordHidden) {
                passwordHidden.type = 'text'
                passwordVisible.innerText = 'hide'
            } else {
                passwordHidden.type = "password"
                passwordVisible.innerText = 'show'
            }
            isPasswordHidden = !isPasswordHidden;
        }

        // Add a click event listener to the password reveal button
        passwordVisible.addEventListener('click', togglePasswordVisibility);
    });
// Function to load tooltip data when hovering over the Nutrition button
function loadTooltipData(button) {
    const nutritionUrl = button.getAttribute('data-nutrition-url');
    const preparationTime = button.getAttribute('data-preparation-time');
    const title = button.getAttribute('data-recipe-title');
    const image = button.getAttribute('data-recipe-image');

    // Update the tooltip content with nutrition and preparation time information
    $(button).attr('data-original-title', `Preparation Time: ${preparationTime} minutes`);
    $(button).tooltip('show');

    // Fetch nutrition data and update the modal
    fetch(nutritionUrl)
        .then((response) => response.json())
        .then((data) => {
            // Update modal content with nutrition details
            $('#calories').text(data.calories);
            $('#fat').text(data.fat);
            $('#protein').text(data.protein);
            $('#carbohydrates').text(data.carbohydrates);

            // Set the recipe title in the modal
            $('#modalRecipeTitle').text(title);
        })
        .catch((error) => {
            console.error('Error fetching nutrition data:', error);
        });
}

// Initialize tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// Close modal and reset its content when closed
$('#nutritionModal').on('hidden.bs.modal', function (e) {
    // Reset modal content
    $('#calories').empty();
    $('#fat').empty();
    $('#protein').empty();
    $('#carbohydrates').empty();
    $('#modalRecipeTitle').empty();
});
