
console.log('In main.js!');

var usernameInput = document.querySelector('#username')

// // const localVideo = document.getElementById('local-Video');
// // const remoteVideo = document.getElementById('remoteVideo');
// // const startButton = document.getElementById('startButton');

var btnJoin = document.querySelector('#btn-join');

var username;
var webSocket;

function WebSocketOnMessage(event){
   var parsedData = JSON.parse(event.data);
   var message = parsedData['message'];

   console.log('message',message);
}
// let localStream;
// let remoteStream;
// let peerConnection;

btnJoin.addEventListener('click',() => {
     username=usernameInput.value;

      console.log('username',username);
    
     if (username=='')
     {
        return;
     }
     usernameInput.value='';
     usernameInput.disabled= true;
     usernameInput.style.visibility='hidden';

     btnJoin.disabled = true;
     btnJoin.style.visibility='hidden';

     var labelUsername = document.querySelector('#label-username');
     labelUsername.innerHTML = username;
     
     
     var loc = window.location;

     var wsStart = 'ws://';

     if (loc.protocol == 'https:') {
         wsStart = 'wss://';
      }

     var endPoint = wsStart + window.location.host + '/';



     console.log('endPoint : ',endPoint); 

     webSocket = new WebSocket(endPoint);

     webSocket.addEventListener('open',(e) => {
         console.log('connection opened!');
     });

     webSocket.addEventListener('message',WebSocketOnMessage);
     webSocket.addEventListener('close',(e)=>{
      console.log('connection closed!');
  });
     webSocket.addEventListener('error',(e)=>{
      console.log('connection error!');
  });

});

// async function startButton() {
//     localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
//     localVideo.srcObject = localStream;

//     // Implement WebRTC peer connection and signaling here
// }
