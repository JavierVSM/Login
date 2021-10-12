Login and Registration

 - Create a new Flask project
 
 - Create a new MySQL database with a table and the appropriate fields.
 
 - The root route should display a template with the login and registrations forms.
 
 - Validate the registration input.
 
 - If registration is invalid errors messages should be displayed on the index page.
 
 - If registrations is valid, hash the password and save the user in the database, store the user in session and then redirect to the success page.
 
 - Validate the login input  If the login is invalid, display an error message on the index page  If login is valid, store the user in session and then redirect to the success page.
 
 - Add a functioning logout button to the success page that clears session.
 
 - After logging out, ensure you cannot reach the success page.
 - NINJA Bonus: Add an additional validation on passwords to have a least 1 number and 1 uppercase letter.
 
 - SENSEI Bonus: Add additional input types on the form. Get creative with you validations! (Consider including a date picker, radio buttons and/or checkboxes)
