const messageForm = document.getElementById('send-container');
const messageInput = document.getElementById('message-input');
const messageContainer = document.getElementById('message-container');

appendMessage('Private Chat mode');

var socket = new WebSocket('ws://' + window.location.host + WS_URL);
var SecondPublicKey = '';
var RSAkey = ''
console.log(RSAkey);


function appendMessage(message) {
    const messageElement = document.createElement('div')
    messageElement.innerText = message
    messageContainer.append(messageElement)
    messageElement.scrollIntoView()
}

function your_appendMessage(message) {
    const messageElement = document.createElement('div')
    messageElement.innerText = message
    messageElement.style.backgroundColor = "beige";
    messageElement.style.margin = ".3em 0 .3em 30vw"
    messageContainer.append(messageElement)
    messageElement.scrollIntoView()
}

socket.onopen = function() {
    appendMessage('You connected');

    var array = new Uint32Array(2);
    window.crypto.getRandomValues(array);
    var PassPhrase = '' + array[0] + array[1];
    console.log(PassPhrase)
    var Bits = 1024; 
    RSAkey = cryptico.generateRSAKey(PassPhrase, Bits);
    var PublicKeyString = cryptico.publicKeyString(RSAkey);
    appendMessage('Keys has been generated');
    appendMessage('Please wait for the connection with your interlocutor');
    socket.send(`PublicKey:${PublicKeyString}`);
  };

socket.onclose = function(event){
    if(event.wasClean){
        appendMessage('Clean connection end')
    }else{
        appendMessage('Connection broken')
    }
};

socket.onmessage = function(event) {
    var message = event.data;
    if (message.startsWith('PublicKey:')) {
        SecondPublicKey = message.slice(10);
        appendMessage('Сonnection with your interlocutor has been established!');
    }
    else {
        var DecryptionResult = cryptico.decrypt(message, RSAkey);
        if (DecryptionResult.plaintext === undefined) {
            appendMessage(message);
        }
        else {
            if (DecryptionResult.signature === 'verified') {
                appendMessage(DecryptionResult.plaintext);
            }
            else {
                appendMessage('Message is not verified!');
            }
        }
    }
    
};

messageForm.addEventListener('submit', e => {
    e.preventDefault()
    const message = messageInput.value
    your_appendMessage(`${message}`)
    var EncryptionResult = cryptico.encrypt(message, SecondPublicKey, RSAkey);
    socket.send(EncryptionResult.cipher);
    messageInput.value = ''
})

