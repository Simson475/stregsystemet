d = new Date();
if(d.getMonth() === 10){
    for(let snowflakes=0; snowflakes < d.getDate(); snowflakes++){
        spawn_snowflake();
    }
    const santa = document.createElement('div');
    santa.classList.add("santa");
    const gif = document.createElement("img")
    gif.src="https://www.animatedimages.org/data/media/359/animated-santa-claus-image-0420.gif";
    santa.appendChild(gif);
    document.body.querySelector(".snow-container").appendChild(santa);

    const bodyStyle =document.body.style;
    bodyStyle.color="white";
    bodyStyle.backgroundImage="url(\""+media_url+"stregsystem/background.jpg\")";
    bodyStyle.backgroundRepeat="repeat-x";
    bodyStyle.backgroundSize="auto 100%";
    bodyStyle.padding="0";
    bodyStyle.margin="0";
    bodyStyle.width="100vw";
    bodyStyle.height="100vh";
    bodyStyle.position="relative"
}

function spawn_snowflake () {
    const snowflake = document.createElement('div');
    snowflake.classList.add("snowflake");
    document.body.querySelector(".snow-container").appendChild(snowflake);
}