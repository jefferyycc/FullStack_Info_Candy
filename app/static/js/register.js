function checkUserName() {
      $.ajax({
      url : "http://localhost:5002/checkemail",// your username checker url
      type : "POST",
      dataType :"json",
      data : {"email": $("#email").val()},
      success : function (data) {
        if(data == "success")
          {$(".success").show();$(".success").text("Email is OK to use."); $("#submit").prop("disabled",false);}
        else
          {$(".success").show();$(".success").text("Email already exists."); $("#submit").prop("disabled",true);}
      }
    });
}