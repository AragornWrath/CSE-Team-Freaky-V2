function dropdown(){
    if (document.getElementById("dropdown").className == "dropdown-hidden"){
        document.getElementById("dropdown").className = "dropdown-show";
    }
    else {
        document.getElementById("dropdown").className = "dropdown-hidden";
    }
}

function likeButton(){
    like_button = document.getElementById("likeButton")
    if (like_button.className == "like-button-unclicked") { 
        like_button.innerHTML = '<img id="likeButtonImage" class="like-button-clicked-image" src="/static/home/icons/red_heart.svg">' ;
        like_button.className = "like-button-clicked";
    }
    else {
        like_button.innerHTML = '<img id="likeButtonImage" class="like-button-unclicked-image" src="/static/home/icons/empty_heart.svg">' ;
        like_button.className = "like-button-unclicked";
    }
}

function viewLikes(){
    
}

function addLike(tripID){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updateLike(this.response, tripID);
            console.log(this.response);
        }
    }
    const likeJSON = {"tripID": tripID};
    request.open("POST", "add-like");
    request.send(JSON.stringify(likeJSON));
}

function updateLike(response, tirpID){

}