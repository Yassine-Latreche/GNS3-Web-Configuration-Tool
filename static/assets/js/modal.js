var modal = $('#modal-1');

function closeModal() {
    $('#modal-1').modal('hide');
}

$(document).on("click",".editConnection", async function () {
    let id = $(this).attr("data-id");
    $('#modal-form').attr('action', `/connections/${id}`);
    $('#modal-form').attr('method', 'POST');
    let conn;
    await $.get(`/connections/${id}`, function( data ) {
        console.log(data[0]["fields"]);
        conn = data[0]["fields"];
    });
    modal.find("#modal-title").text("Edit a connection")
    modal.find("#submit-btn").text("Edit")
    modal.find("#ip_address").val(conn.ip_address);
    modal.find("#port").val(conn.port);
    $('#modal-1').modal('show');
});

$(document).on("click","#create_modal_button", async function () {
    $('#modal-form').attr('action', '/connections/create');
    $('#modal-form').attr('method', 'POST');
    modal.find("#modal-title").text("Create a connection")
    modal.find("#submit-btn").text("Create")
    modal.find("#ip_address").val("");
    modal.find("#port").val("");
    $('#modal-1').modal('show');
});