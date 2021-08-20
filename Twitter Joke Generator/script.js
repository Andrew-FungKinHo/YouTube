function getNewJoke(){
    // send a GET request to the joke API
    const request = new Request("https://official-joke-api.appspot.com/jokes/programming/random");
    fetch(request)
    .then(res => {return res.json();})
    .then(result => {
        console.log(result[0].setup);
        console.log(result[0].punchline);

        // change the div elements on the UI
        var dateTime = getDateTime();

        document.getElementById('jokeSetupText').innerHTML = result[0].setup;
        document.getElementById('jokePunchlineText').innerHTML = result[0].punchline;
        document.getElementById('dateTime').innerHTML = 
        `${dateTime[0]} &middot; ${dateTime[1]} <span>Twitter for iPhone</span>`
    });
}

function getDateTime(){
    // get correct date format
    const months = ["Jan", "Feb", "Mar","Apr", "May", "Jun", "July", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var today = new Date();
    var date = months[(today.getMonth())] + ' '+ today.getDate()+', '+today.getFullYear();

    // get correct timestamp format
    var hours = today.getHours();
    var minutes = today.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12 ;// the hour '0' should be 12
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var time = hours + ':' + minutes + ' '+ ampm;

    console.log(date);
    console.log(time);

    return [time,date]
}