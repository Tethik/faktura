$(document).ready(function() {

  inputRow = '<tr> ' +
            '<td><input type="text" name="key"></td> ' +
            '<td><input type="text" name="value"></td> ' +
            '<td><button class="button-primary" name="createVar" name="remove-row" type="button">create</button></td> ' +
          '</tr>';

  saveNdelbuttons = '<button name="saveVar" class="button-primary">save</button><button name="deleteVar" class="button">delete</button>';

  function bindButtons() {
    $("button[name='createVar']").click(function() {
      row = $(this).closest("tr");
      cell = $(this).closest("td");
      key = $(row).find("input[name='key']").val();
      $(row).find("input[name='key']").attr("disabled", "disabled"); //key is now immutable.
      value = $(row).find("input[name='value']").val();

      dataz = { "key": key, "value": value };
      console.log(dataz);
      $.post("/vars/create", dataz, function(data) {
        cell.html(saveNdelbuttons);
        bindButtons();
      }, "json");
    });

    $("button[name='saveVar']").click(function() {
      row = $(this).closest("tr");
      key = $(row).find("input[name='key']").val();
      value = $(row).find("input[name='value']").val();
      $.post("/vars/save", { "key": key, "value": value }, "json");
    });

    $("button[name='deleteVar']").click(function() {
      row = $(this).closest("tr");
      key = $(row).find("input[name='key']").val();
      $(row).find("input[name='key']").attr("disabled", "disabled"); //key is now immutable.
      value = $(row).find("input[name='value']").val();
      row.remove();
      $.post("/vars/delete", { "key": key });

    });
  };

  $("#newVar").click(function() {
    $("#template-var-rows").append(inputRow);
    bindButtons();
  });

  bindButtons();
});
