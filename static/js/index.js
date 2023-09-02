let groupName = document.querySelector("#room_name").innerHTML;
let username = document.querySelector("#user_name").innerHTML;
let user2name=document.querySelector("#admin_username").innerHTML
let useradmin=JSON.parse(user2name)
let state=document.querySelector("#room_state").innerHTML
state=JSON.parse(state)
let url =
  "ws://" + window.location.host + "/" + "ws/live_music/" + groupName + "/";
let ws = new WebSocket(url);
let roomTime=document.querySelector("#room_time").innerHTML;
console.log(roomTime)

console.log(groupName);
console.log(username);
let videoplayer=document.querySelector('.audio_player')
roomTime=parseFloat(roomTime)
videoplayer.currentTime=roomTime
console.log(typeof(roomTime))
ws.onopen = function (event) {
  console.log("connection establised");
};
ws.onmessage = function (event) {
  let data = JSON.parse(event.data);
  console.log("message received from user", data.message);
  let message=data.message
  if(data.message.constructor===String){
    display_message(data.message,data.username)
  }
  if(message=='disabled'){
    window.history.go(-1)
    setTimeout(function(){
      window.location.reload()
    },2000)
  }
  admin_controls(message)
};
ws.onerror = function (event) {
  console.log("an error occurred", event);
};
ws.onclose = function (event) {
  console.log("connection disconnected");
};
let chatbox = document.querySelector("#chat");
let send_btn = document.querySelector(".send-btn");
send_btn.addEventListener("click", () => { 
  send_message()
});
chatbox.addEventListener('keypress',(e)=>{
  if(e.key=='Enter'){
    send_message()
  }
})
function send_message(){
  if(chatbox.value!=""){
    ws.send(JSON.stringify({ "message": chatbox.value,"username":username }));
    chatbox.value=""
   }
   else{
    chatbox.focus()
   }
}

// videoplayer.addEventListener('pause',()=>{
//   ws.send(JSON.stringify({'message':'pause','username':username}))
// })
// videoplayer.addEventListener('play',()=>{
//   ws.send(JSON.stringify({'message':'start','username':username}))
// })
function admin_controls(message){
  if(message==false){
    videoplayer.pause()
  }
  else if(message==true){
    videoplayer.play()
  }
  else if(!isNaN(message)){
    console.log("got the number from server")
    videoplayer.duration=message
    // if(videoplayer.currentTime>=message){
    //   forwardB
      
    // }
  }

}


let overlay=document.querySelector('.overlay')
if(username==user2name){
  overlay.style.display='none'
  // this is to prevent the admin from reloading the page
  // window.addEventListener('beforeunload',(e)=>{       
  //   e.preventDefault()
  //   e.returnValue="";
  // })

  videoplayer.addEventListener('timeupdate',()=>{
    let currentTime=videoplayer.currentTime
    ws.send(JSON.stringify({'message':currentTime,'username':username}))
  })
  videoplayer.addEventListener('play',()=>{
    ws.send(JSON.stringify({'message':true,'username':username}))

  })
  videoplayer.addEventListener('pause',()=>{
    ws.send(JSON.stringify({'message':false,'username':username}))
  })
}
if(state==true){
  videoplayer.play()
}
else if(state==false){
  videoplayer.pause()
}

function display_message(message,username){
  let messageoutterbox=document.querySelector("#messagecontbox")
  let messagecont=document.createElement('p')
  let messagebox=document.createElement('div')
  let user_info=document.createElement('h6')
  user_info.classList.add("card-title")
  if(username===useradmin){
    user_info.innerHTML=`admin : ${useradmin}`

  }
  else{
    user_info.innerHTML=`${username}`
  }
  messagebox.insertAdjacentElement('afterbegin',user_info)
  messagebox.classList.add('card')
  messagecont.classList.add("card-text")
  messagecont.innerText=`${message}`
  messagebox.appendChild(messagecont)
  messageoutterbox.insertAdjacentElement('beforeend',messagebox)
  messageoutterbox.scrollTop=messageoutterbox.scrollHeight

}