function addLogMessage(id, json) {
        console.log("Got the message... " + id);
        console.log(json)
        $('#'+id).children().prepend(json['html']);
}
