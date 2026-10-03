
codesquaresize = 150;
qrcode = new QRCode(document.getElementById("qrcode"), {
	text: window.location.href,
	width: codesquaresize,
	height: codesquaresize,
	colorDark : "#000000",
	colorLight : "#ffffff",
	correctLevel : QRCode.CorrectLevel.H
});

feed = [];

document.getElementById("post").value = "";
document.getElementById("post").select();

document.getElementById("clear").onclick = function(){

    feed = [];
    loadFeed();
    saveFeed();
    document.getElementById("post").value = "";
    document.getElementById("post").select();
    
}

document.getElementById("post").onchange = function(){
    if(this.value.slice(-5) == ".html" || this.value.slice(0,8) == "https://" || this.value.slice(0,8) == "HTTPS://" || this.value.slice(0,7) == "http://"){
        post = "<a href = \"" + this.value + "\">" + this.value + "</a>";
    }
    else{
        post = this.value;
    }
    feed.unshift(post);
    this.value = "";
    loadFeed();
    saveFeed();
}

load_file('feed.json').then(
    raw_feed => {
        feed = JSON.parse(raw_feed);
        loadFeed();
    }
);

function loadFeed(){

    document.getElementById("feed").innerHTML = "";
    for(let index = 0;index < feed.length;index++){
        let newSign = document.createElement("DIV");
        newSign.id = "sign-" + index.toString();
        newSign.className = "sign";
        newSign.innerHTML = feed[index];
        let deleteButton = document.createElement("SPAN");
        deleteButton.className = "delete-button";
        deleteButton.innerHTML = "DELETE";
        deleteButton.onclick  = function(){
            let localIndex = parseInt(this.parentNode.id.split("-")[1]);
            let newFeed = [];
            for(let index = 0;index < feed.length;index++){
                if(index != localIndex){
                    newFeed.push(feed[index]);
                }
            }
            feed = newFeed;
            saveFeed();
            loadFeed();
        }
        newSign.appendChild(deleteButton);
        document.getElementById("feed").appendChild(newSign);
    }
}

function saveFeed(){
    data = encodeURIComponent(JSON.stringify(feed,null,"   "));
    save_file("feed.json",data);
}

function setup() {
    frameRate(3);
}

function draw(){
    //load feed
    feedLength = feed.length;
    load_file('feed.json').then(
    raw_feed => {
        feed = JSON.parse(raw_feed);
        if(feedLength != feed.length){
            loadFeed();
        }
    });
}

function load_file(name) {
    return fetch('load-file.php?filename=' + name).then(res => res.text());
}


function save_file(name,data){
    fetch('save-file.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
        body: 'data=' + data + '&filename=' + name
    });
}

