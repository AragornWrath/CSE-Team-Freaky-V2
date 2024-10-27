/* Ajax for creating a trip */
/* trip date will be sent as 'yyyy-mm-dd' */

function addTrip(){
    const tripNameTextBox = document.getElementById("trip-name-text-box");
    const tripName = tripNameTextBox.value;

    const tripDestinationTextBox = document.getElementById("trip-destination-text-box");
    const tripDestination = tripDestinationTextBox.value;

    const dateBox = document.getElementById("date-box");
    const date = dateBox.value;

    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            //CALL UPDATE TRIPS POTENTIALLY INSTEAD OF CONSOLE.LOG
            console.log(this.response);
        }
    }
    const tripJSON = {"tripName": tripName, "tripDestination": tripDestination, "date": date};
    request.open("POST", "/add-trip");
    request.send(JSON.stringify(tripJSON));
}

/* Model ajax from jesse*/
function sendChat() {
    const chatTextBox = document.getElementById("chat-text-box");
    const xsrf_token = document.getElementById("xsrf_token")
    const token_val = xsrf_token.value
    const message = chatTextBox.value;
    chatTextBox.value = "";
    if (ws) {
        // Using WebSockets
        socket.send(JSON.stringify({'messageType': 'chatMessage', 'message': message, 'xsrf-token': token_val}));
    } else {
        // Using AJAX
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(this.response);
            }
        }
        const messageJSON = {"message": message, "xsrf-token": token_val};
        request.open("POST", "/chat-messages");
        request.send(JSON.stringify(messageJSON));
    }
    chatTextBox.focus();
}