const messageForm = document.getElementById('send-container');
const messageInput = document.getElementById('message-input');
const messageContainer = document.getElementById('message-container');

appendMessage('Private Chat mode');

var socket = new WebSocket('ws://' + window.location.host + WS_URL);

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
  };

socket.onclose = function(event){
    if(event.wasClean){
        appendMessage('Clean connection end')
    }else{
        appendMessage('Connection broken')
    }
};

socket.onmessage = function(event) {
    console.log(event.data)
    var message = event.data;
    if (message.startsWith(`${user_name}:`)) {
        message = message.split(":").pop();
        if (message === " " || message === "  ") {your_appendMessage(`[empty message ${message}]`);}
        else {
            your_appendMessage(`${message}`);
        }
    }
    else {
        appendMessage(event.data)
    }
};

messageForm.addEventListener('submit', e => {
    e.preventDefault()
    const message = messageInput.value
    your_appendMessage(`${message}`)
    socket.send(message);
    messageInput.value = ''
})

