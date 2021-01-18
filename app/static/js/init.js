(function($){
  $(document).ready(function(){

    $.fn.getFormData = function(){
      const formData = {}
      if( this && this[0].tagName == "FORM" ){
        const $form = $(this[0]);

        const selectors = [
          'input[type="text"][name]:not([disabled])',
          'input[type="date"][name]:not([disabled])',
          'input[type="time"][name]:not([disabled])',
          'input[type="number"][name]:not([disabled])',
          'input[type="radio"][name]:checked:not([disabled])',
          'select[name]:not([disabled])',
          'textarea[name]:not([disabled])'
        ];

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

    // Initialize Time Picker
    $('input.timepicker').timepicker({
      showClearBtn: true,
      twelveHour: false,
      defaultTime: 'now',
      fromNow: 5*60*1000,
      duration: 1,
      autoClose: true,
    });
    $("input.timepicker").each(function(idx, elem){
      const instance = M.Timepicker.getInstance(elem);
      instance._updateTimeFromInput();
      instance.done();
    });

    // Initialize input type 'date'
    $('input[type="date"]').each(function(idx, elem){
      const now = new Date();

      let year = now.getFullYear();
      let month = now.getMonth()+1;
      let day = now.getDate();

      let monthFmt = String(month);
      if( month < 10 ){
        monthFmt = "0"+monthFmt;
      }
      let dayFmt = String(day);
      if( day < 10 ){
        dayFmt = "0"+dayFmt;
      }
      
      $(elem).val(year+"-"+monthFmt+"-"+dayFmt);
    });

    // Initialize input type 'time'
    $('input[type="time"]').each(function(idx, elem){
      const fromNow = 5;
      const now = new Date(new Date().getTime() + ( fromNow * 60 * 1000));

      let hours = now.getHours();
      let minutes = now.getMinutes();
      let seconds = now.getSeconds();
      
      let hoursFmt = String(hours);
      if( hours < 10 ){
        hoursFmt = "0"+hoursFmt;
      }

      let minutesFmt = String(minutes);
      if( minutes < 10 ){
        minutesFmt = "0"+minutesFmt;
      }

      let secondsFmt = String(seconds);
      if( seconds < 10 ){
        secondsFmt = "0"+secondsFmt;
      }

      $(elem).val(hoursFmt+":"+minutesFmt+":"+secondsFmt);
    });

    
    // Initialize Tabs
    $(".tabs").tabs();

  }); // end of document ready
})(jQuery); // end of jQuery name space
