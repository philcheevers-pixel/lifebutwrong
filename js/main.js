document.addEventListener("DOMContentLoaded", function () {
  var forms = document.querySelectorAll(".newsletter-form");
  forms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var input = form.querySelector('input[type="email"]');
      if (!input || !input.value) {
        return;
      }
      alert(
        "Newsletter signup is not connected yet. Replace this form with your Beehiiv or Substack embed."
      );
    });
  });
});
