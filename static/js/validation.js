

function isValidAlphaSpace(value) {
    const regex = /^[A-Za-z\s]+$/;
    return regex.test(value);
}

function displayError(element, message) {
    const errorElement = document.createElement('div');
    errorElement.classList.add('alert', 'alert-danger', 'js-error');
    errorElement.innerText = message;
    element.parentNode.insertBefore(errorElement, element.nextSibling);
}
document.addEventListener("DOMContentLoaded", function() {

    const form = document.querySelector('form');

    form.addEventListener("submit", function(event) {

        // Clear previous error messages
        const errorElements = document.querySelectorAll('.js-error');
        errorElements.forEach(el => el.remove());

        // ClassInfoForm
        validateField('#id_name', isValidAlphaSpace, "Name should only contain alphabets and spaces.");
        validateField('#id_display_name', isValidAlphaSpace, "Display name should only contain alphabets and spaces.");

        // ResourceForm
        validateField('#id_resource_title', isValidAlphaSpace, "Resource title should only contain alphabets and spaces.");

        // SectionForm
        validateField('#id_name', isValidAlphaSpace, "Name should only contain alphabets and spaces.");

        // GuideTeacherForm
        validateField('#id_name', isValidAlphaSpace, "Name should only contain alphabets and spaces.");

        // PersonalInfoForm
        validateField('#id_name', isValidAlphaSpace, "Name should only contain alphabets and spaces.");
        validateField('#id_phone_no', isValidPhoneNumber, "Phone number should be in the format: '+999999999'.");

        // GuardianInfoForm
        validateField('#id_father_name', isValidAlphaSpace, "Father's name should only contain alphabets and spaces.");
        validateField('#id_mother_name', isValidAlphaSpace, "Mother's name should only contain alphabets and spaces.");

        // EmergencyContactDetailsForm
        validateField('#id_emergency_guardian_name', isValidAlphaSpace, "Emergency guardian name should only contain alphabets and spaces.");

        // PreviousAcademicInfoForm
        validateField('#id_institute_name', isValidAlphaSpace, "Institute name should only contain alphabets and spaces.");
        validateField('#id_name_of_exam', isValidAlphaSpace, "Name of exam should only contain alphabets and spaces.");

        // AddDesignationForm
        validateField('#id_name', isValidAlphaSpace, "Name should only contain alphabets and spaces.");

    });

});

function isValidAlphaSpace(value) {
    const regex = /^[A-Za-z\s]+$/;
    return regex.test(value);
}

function isValidPhoneNumber(value) {
    const regex = /^\+?\d{10}$/;
    return regex.test(value);
}

function validateField(selector, validationFunction, errorMessage) {
    const element = document.querySelector(selector);
    if (element && !validationFunction(element.value)) {
        displayError(element, errorMessage);
        event.preventDefault();
    }
}

function displayError(element, message) {
    const errorElement = document.createElement('div');
    errorElement.classList.add('alert', 'alert-danger', 'js-error');
    errorElement.innerText = message;
    element.parentNode.insertBefore(errorElement, element.nextSibling);
}
