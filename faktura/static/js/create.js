$(document).ready(function() {

parts = document.documentURI.split('/')
customer_id = parseInt(parts[parts.length - 1]);

$("#button-preview").click(function() {
  $("#preview").show();
  $("form").attr("target", "preview")
  $("form").attr("action", "/invoice/render/"+customer_id)
})

$("#button-create").click(function() {
  $("form").attr("target", "")
  $("form").attr("action", "/invoice/create/for_customer/" + customer_id)
})

inputRow = '<tr> ' +
          '<td><input type="text" name="description" placeholder="Atomic screwdriver"></td> ' +
          '<td><input type="text" name="tax" value="25%"></td> ' +
          '<td><input type="number" name="value" placeholder="1337"></td> ' +
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

$('#customerSelect').change(function() {
  val = $("#customerSelect").val();
  if(val != "-1") {
    $.getJSON("/customer/" + val + "/json").done(function(data) {
      console.log(data);
      data = data.customer;
      $("input[name='customerName']").val(data.name);
      $("input[name='customerStreet']").val(data.street);
      $("input[name='customerCity']").val(data.city);
      $("input[name='customerZip']").val(data.zip);
      $("#customerForm input").attr("disabled", "disabled");
    });
  } else {
    $("input[name='customerName']").val("");
    $("input[name='customerStreet']").val("");
    $("input[name='customerCity']").val("");
    $("input[name='customerZip']").val("");
    $("#customerForm input").removeAttr("disabled");
  }
});

$("#invoice-rows").append(inputRow);

$("#preview").hide()
  bindRowRemoval()
});
