$(document).ready(function() {

  $("#button-preview").click(function() {
    $("#preview").show();
    $("form").attr("target", "preview")
    $("form").attr("action", "/render")
  })

  $("#button-create").click(function() {
    $("form").attr("target", "")
    $("form").attr("action", "/create")
  })

  inputRow = '<tr> ' +
            '<td><input type="text" name="description" placeholder="Atomic screwdriver"></td> ' +
            '<td><input type="text" name="vat" value="25%"></td> ' +
            '<td><input type="number" name="cost" placeholder="1337"></td> ' +
            '<td><input class="button-primary" name="remove-row" type="button" value="Remove"></td> ' +
          '</tr>';

  function bindRowRemoval() {
    $("input[name='remove-row']").click(function() {
      $(this).parent().parent().remove()
    })
  }

  $("#button-new-row").click(function() {
    $("#invoice-rows").append(inputRow);
    bindRowRemoval()
  })

  $("#invoice-rows").append(inputRow);

  $("#preview").hide()
  bindRowRemoval()
});
