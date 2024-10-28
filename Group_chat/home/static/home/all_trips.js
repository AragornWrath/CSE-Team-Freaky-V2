function dropdown(){
    if (document.getElementById("dropdown").className == "dropdown-hidden"){
        document.getElementById("dropdown").className = "dropdown-show";
    }
    else {
        document.getElementById("dropdown").className = "dropdown-hidden";
    }
}

function likeButton(tripID){
    like_button = document.getElementById("likeButton_" + tripID)
    if (like_button.className == "like-button-unclicked") { 
        like_button.innerHTML = '<img id="likeButtonImage" class="like-button-clicked-image" src="/static/home/icons/red_heart.svg">' ;
        like_button.className = "like-button-clicked";
        addLike(tripID);
    }
    else {
        like_button.innerHTML = '<img id="likeButtonImage" class="like-button-unclicked-image" src="/static/home/icons/empty_heart.svg">' ;
        like_button.className = "like-button-unclicked";
        deleteLike(tripID);
    }
}

function viewLikes(tripID){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            addViewLikesHTML(this.response, tripID);
            console.log(this.response);
        }
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    const likeJSON = {"tripID": tripID};
    request.open("POST", "view-likes");
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(likeJSON))
}

function addViewLikesHTML(response, tripID){
    parsed_response = JSON.parse(response);
    likes_list = parsed_response["likes"]
    let html = "<ul>"
    for (let liker of likes_list){
        html += createViewLikesHTML(liker)
    }
    html += "</ul>"
    likes_popup = document.getElementById("likes_popup");
    likes_popup.innerHTML = html
    console.log(html)
}

function createViewLikesHTML(liker){
    const html = "<li>" + liker + "</li>"
    return html
}

function addLike(tripID){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updateLikes(this.response, tripID);
            console.log(this.response);
        }
    }
    const likeJSON = {"tripID": tripID};
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    request.open("POST", "add-like");
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(likeJSON));
}

function updateLikes(response, tripID){  
    parsed_response = JSON.parse(response);
    likes_list = parsed_response["likes"]
    numberOfLikes = likes_list.length;
    likes = document.getElementById("number-of-likes_" + tripID);
    likes.innerHTML = numberOfLikes;
}

function deleteLike(tripID){
    const request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updateLikes(this.response, tripID);
            console.log(this.response);
        }
    }
    const likeJSON = {"tripID": tripID};
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    request.open("POST", "delete-like");
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(likeJSON));
}