
console.log('In main.js!');

var usernameinput = document.getElementById('#username')

// const localVideo = document.getElementById('local-Video');
// const remoteVideo = document.getElementById('remoteVideo');
// const startButton = document.getElementById('startButton');

var btnJoin = document.getElementById('#btn-join');

var username;
let localStream;
let remoteStream;
let peerConnection;

btnJoin.addEventListener('click',() => {
    username=usernameinput.value;

    
     if (username=='')
     {
        return;
     }
     usernameinput.value='';
     usernameinput.disabled= true;
     usernameinput.style.visibility='hidden';

     btnJoin.disabled = true;
     btnJoin.style.visibility='hidden';

     var labelUsername = document.querySelector('#h3-username');
     labelUsername.innerHTML = username;
     
     
     var loc = window.location;
     var wsstart='wss://';

     if(loc.protocol== 'https:'){
        wsstart = 'wss://';
     }
    
     var endPoint = wsstart + loc.host + loc.pathname;

     console.log('endPoint : ',endPoint); 



});

// async function startButton() {
//     localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
//     localVideo.srcObject = localStream;

//     // Implement WebRTC peer connection and signaling here
// }
