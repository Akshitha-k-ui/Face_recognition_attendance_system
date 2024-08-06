
document.addEventListener("DOMContentLoaded", function() {
  // Select the read more link
  var readMoreLink = document.querySelector('.read-more');

  // Add click event listener to the read more link
  readMoreLink.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default link behavior

    // Select the hidden content
    var hiddenContent = document.querySelector('.hidden-content');

    // Toggle the visibility of the hidden content
    hiddenContent.classList.toggle('show');
    
    // Change the text of the read more link based on visibility
    if (hiddenContent.classList.contains('show')) {
      readMoreLink.textContent = 'Read Less';
    } else {
      readMoreLink.textContent = 'Read More';
    }
  });
});
