function dropdown(){
    if (document.getElementById("dropdown").className == "dropdown-hidden"){
        document.getElementById("dropdown").className = "dropdown-show";
    }
    else {
        document.getElementById("dropdown").className = "dropdown-hidden";
    }
}

function addTripPopUp(){
    if (document.getElementById("addTripCard").className == "dropdown-hidden"){
        document.getElementById("addTripCard").className = "add-trip-card";
    }
    else {
        document.getElementById("addTripCard").className = "dropdown-hidden";
    }
}

/* Ajax for creating a trip */
/* trip date will be sent as 'yyyy-mm-dd' */

function addTrip(){
    const tripNameTextBox = document.getElementById("trip-name-text-box");
    const tripName = tripNameTextBox.value;
    tripNameTextBox.value = "";

    const tripDestinationTextBox = document.getElementById("trip-destination-text-box");
    const tripDestination = tripDestinationTextBox.value;
    tripDestinationTextBox.value = "";

    // const dateBox = document.getElementById("date-box");
    // const date = dateBox.value;

    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            addTripToHTML(this.response);
            console.log(this.response);
        }
    }
    const tripJSON = {"tripName": tripName, "tripDestination": tripDestination};

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
    request.open("POST", "add-trip/");
    request.setRequestHeader("X-CSRFToken", csrftoken)
    request.send(JSON.stringify(tripJSON));
}

//When adding a trip use "afterbegin" so that way the add trip button is pushed to the end
function addTripToHTML(response){
    const trips = document.getElementById("tripsTable");
    const parsed_response = JSON.parse(response)
    const trips_list = parsed_response["trips"]
    for (let trip of trips_list){
        const tripName = trip["tripname"]
        const tripDestination = trip["destination"]
        trips.insertAdjacentHTML("afterbegin", createTripHTML(tripName, tripDestination))
    }
}

function createTripHTML(tripName, tripDestination){
    let html = '<div class="trip"> <div class="trip-header"> <b class="trip-title">' + tripName + '</b> </div> <b class="trip-destination">' + tripDestination + '</b> </div>'
    return html
}

/* Model ajax from jesse*/