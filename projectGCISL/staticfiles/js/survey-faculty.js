

// drop down filter
function dropDownSurveyTitle() {
    // Get a reference to the select element
    const elem = document.getElementById('survey-titles');
  
    // Add an event listener to the select element
    elem.addEventListener('change', function() {
        // Submit the form when a selection is made
        document.getElementById('filter-form').submit();
    });
  }
  
  
  
  
  