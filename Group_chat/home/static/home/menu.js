function dropdown(){
    if (document.getElementById("dropdown").className == "dropdown-hidden"){
        document.getElementById("dropdown").className = "dropdown-show";
    }
    else {
        document.getElementById("dropdown").className = "dropdown-hidden";
    }
}

function onload(){
    initWS();
}

function initWS(){
    let url = 'ws://' + window.location.host + '/scheme'
    socket = new WebSocket(url)

    socket.onmessage = function (ws_message) {
        likes_data = JSON.parse(ws_message.data)
        // console.log("likes data ->")
        // console.log(likes_data)
        message = likes_data["message"]
        // console.log(JSON.parse(ws_message.data))
        updateLikes(ws_message.data, tripID)
    }
}