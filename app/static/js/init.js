(function($){
  $(document).ready(function(){

    $.fn.getFormData = function(){
      const formData = {}
      if( this && this[0].tagName == "FORM" ){
        const $form = $(this[0]);

        const selectors = [
          'input[type="text"][name]:not([disabled])',
          'input[type="radio"][name]:checked:not([disabled])',
          'select[name]:not([disabled])',
          'textarea[name]:not([disabled])'
        ]
        const children = $form.find(selectors.join(','));
    
        children.each(function(idx, elm){
          const $elm = $(this);
          const value = $elm.val();
          const name = $elm.attr("name");
          formData[name] = value;
        });
      }
      return formData;
    }

    M.updateTextFields();
    $('input.text-counter, textarea.text-counter').characterCounter();
    $('select').formSelect();

    $('.sidenav').sidenav();
    $('.parallax').parallax();

    // Initialize Autocomplate input
    $('input.autocomplete').autocomplete({
      data: {
        "Apple": null,
        "Microsoft": null,
        "Google": 'https://placehold.it/250x250'
      },
    });

    // Initialize Date Picker
    $('input.datepicker').datepicker({
      format: "yyyy-mm-dd",
      autoClose: true,
      defaultDate: new Date(),
      setDefaultDate: true,
      minDate: new Date(),
    });

    $('input.timepicker').timepicker({
      showClearBtn: true,
      twelveHour: false,
      defaultTime: 'now',
      fromNow: 60*1000,
      duration: 1,
    });
    
  }); // end of document ready
})(jQuery); // end of jQuery name space
