// Close popup function
function closePopup() {
    var popup = document.getElementById('popup');
    popup.style.display = 'none';
}

// Initialize Toastr options
toastr.options = {
    closeButton: true,
    progressBar: true,
    positionClass: 'toast-top-right',
    timeOut: 5000, // 5 seconds
    preventDuplicates: true, // Prevent duplicate toasts
    newestOnTop: true, // Show newest toast on top
    toastClass: 'toast-error', // Custom class for toastr messages
    toastClass: 'toast-value-name' // Custom class for toastr messages
};

// Initialize form wizard
$("#form-total").steps({
    headerTag: "h2",
    bodyTag: "section",
    transitionEffect: "fade",
    autoFocus: true,
    transitionEffectSpeed: 500,
    titleTemplate: '<div class="title">#title#</div>',
    labels: {
        previous: 'Back',
        next: 'Next',
        finish: 'Confirm',
        current: ''
    },
    onStepChanging: function (event, currentIndex, newIndex) {
        var isValid = true;
        var fields = $("#form-register").find("section").eq(currentIndex).find("input[required], select[required], input[type='number']");

        fields.each(function () {
            var $this = $(this);

            if ($this.is("input[type='number']")) {
                var min = parseFloat($this.attr("min"));
                var max = parseFloat($this.attr("max"));
                var val = parseFloat($this.val());

                if (isNaN(val) || val < min || val > max) {
                    isValid = false;
                    $this.addClass("error");
                    var errorName = $this.attr("error_name");
                    toastr.error("<span class='toast-error-name'>" + errorName + ":</span><br>Value must be between <span class='toast-value-name'>" + min + "</span> and <span class='toast-value-name'>" + max +"</span>");
                    return false; // Stop further iteration
                } else {
                    $this.removeClass("error");
                }
            } else if ($this.is("input[required], select[required]")) {
                if (!$this.val()) {
                    isValid = false;
                    $this.addClass("error");
                    var errorName = $this.attr("error_name");
                    toastr.error("<span class='toast-error-name'>" + errorName + "</span> is required.");
                    return false; // Stop further iteration
                } else {
                    $this.removeClass("error");
                }
            }
        });

        // Update confirmation details on the final step
        if (isValid && newIndex === $("#form-register").find("section").length - 1) {
            var fullname = $('#first_name').val() + ' ' + $('#last_name').val();
            var gender = $('#Gender').val();
            var age = $('#Age').val();
            var address = $('#address').val();
            var Glucose = $('#Glucose').val();
            var Cholesterol = $('#Cholesterol').val();
            var HDL_Chol = $('#HDL_Chol').val();
            var Ratio_Chol_HDL = ($('#Cholesterol').val() / $('#HDL_Chol').val()).toFixed(2);
            var Height = $('#Height').val();
            var Weight = $('#Weight').val();
            var Systolic_BP = $('#Systolic_BP').val();
            var Diastolic_BP = $('#Diastolic_BP').val();
            var Waist = $('#Waist').val();
            var Hip = $('#Hip').val();

            $('#fullname-val').text(fullname);
            $('#gender-val').text(gender);
            $('#age-val').text(age);
            $('#address-val').text(address);
            $('#Glucose-val').text(Glucose);
            $('#Cholesterol-val').text(Cholesterol);
            $('#HDL_Chol-val').text(HDL_Chol);
            $('#Ratio_Chol-val').text(Ratio_Chol_HDL);
            $('#Height-val').text(Height);
            $('#Weight-val').text(Weight);
            $('#Systolic_BP-val').text(Systolic_BP);
            $('#Diastolic_BP-val').text(Diastolic_BP);
            $('#Waist-val').text(Waist);
            $('#Hip-val').text(Hip);
        }

        return isValid;
    },
    onFinished: function (event, currentIndex) {
        $("#form-register").submit();
    }
});

// Datepicker initialization example (if used)
$("#day").datepicker({
    dateFormat: "MM - DD - yy",
    showOn: "both",
    buttonText: '<i class="zmdi zmdi-chevron-down"></i>',
});