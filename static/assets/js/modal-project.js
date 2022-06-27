var modal = $('#modal-1');

function closeModal() {
    $('#modal-1').modal('hide');
}

$(document).on("click",".editProject", async function () {
    let connection_id = $(this).attr("data-connection_id");
    let id = $(this).attr("data-id");
    $('#modal-form').attr('action', `/connections/${connection_id}/projects/${id}`);
    $('#modal-form').attr('method', 'POST');
    let proj;
    await $.get(`/connections/${connection_id}/projects/${id}`, function( data ) {
        proj = data;
    });
    modal.find("#modal-title").text("Edit a connection")
    modal.find("#submit-btn").text("Edit")
    modal.find("#name").val(proj.name);
    $('#modal-1').modal('show');
});

$(document).on("click","#create_modal_button", async function () {
    let connection_id = $(this).attr("data-connection_id");
    $('#modal-form').attr('action', `/connections/${connection_id}/projects/create`);
    $('#modal-form').attr('method', 'POST');
    modal.find("#modal-title").text("Create a connection")
    modal.find("#submit-btn").text("Create")
    modal.find("#ip_address").val("");
    modal.find("#port").val("");
    $('#modal-1').modal('show');
});