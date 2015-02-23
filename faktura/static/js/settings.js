$(document).ready(function() {

  inputRow = '<tr> ' +
            '<td><input type="text" name="key"></td> ' +
            '<td><input type="text" name="value"></td> ' +
            '<td><button class="button-primary" name="createVar" name="remove-row" type="button">create</button></td> ' +
          '</tr>';

  saveNdelbuttons = '<button name="saveVar" class="button-primary">save</button><button name="deleteVar" class="button">delete</button>';

  csrf_token = $("input[name='_csrf_token']").val();

  function bindButtons(elem) {
    $(elem).on("click", "button[name='createVar']", function() {
      row = $(this).closest("tr");
      cell = $(this).closest("td");
      key = $(row).find("input[name='key']").val();
      $(row).find("input[name='key']").attr("disabled", "disabled"); //key is now immutable.
      value = $(row).find("input[name='value']").val();

      dataz = { "key": key, "value": value, "_csrf_token": csrf_token };
      console.log(dataz);
      $.post("/vars/create", dataz, function(data) {
        cell.html(saveNdelbuttons);
        csrf_token = data._csrf_token;
      }, "json");
    });

    $(elem).on("click", "button[name='saveVar']", function() {
      row = $(this).closest("tr");
      key = $(row).find("input[name='key']").val();
      value = $(row).find("input[name='value']").val();
      $.post("/vars/save", { "key": key, "value": value, "_csrf_token": csrf_token }, function(data) {
        csrf_token = data._csrf_token;
      }, "json");
    });

    $(elem).on("click", "button[name='deleteVar']", function() {
      row = $(this).closest("tr");
      key = $(row).find("input[name='key']").val();
      $(row).find("input[name='key']").attr("disabled", "disabled"); //key is now immutable.
      value = $(row).find("input[name='value']").val();
      row.remove();
      $.post("/vars/delete", { "key": key, "_csrf_token": csrf_token }, function(data) {
        csrf_token = data._csrf_token;
      }, "json");

    });
  };

  $("#newVar").click(function() {
    $("#template-var-rows").append(inputRow);
  });

  bindButtons(document);
});
