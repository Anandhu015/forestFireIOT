let progressbar =document.querySelector(".circular-progress");
let valueContainer=document.querySelector(".value-container");
document.getElementById("temp").innerHTML=temperature;

let progressValue=0;
let progressEndValue="{{obj.temp_reading}}";
let speed=10;
let progress=setInterval(() =>{
    progressValue++;
    valueContainer.textContent=`${progressValue}%`;
    progressbar.style.background=`conic-gradient(
        #4d5bf9 ${progressValue *3.6}deg ,
        #cadcff ${progressValue * 3.6}deg
    )`;
    if(progressValue == progressEndValue)
    {
        clearInterval(progress);
    }
})
