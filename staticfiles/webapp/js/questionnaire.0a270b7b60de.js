document.addEventListener('DOMContentLoaded', () => {
  let checkboxes = document.querySelectorAll("input[type=checkbox]");
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });

  // next button disabled by default
  let next_button = document.getElementById('next_button');
  next_button.disabled = true;

  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      let checked = document.querySelectorAll('input[type="checkbox"]:checked');
      next_button.disabled = checked.length < 1;
    });
  });

});