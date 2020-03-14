const messageForm = document.getElementById('send-container');
const messageInput = document.getElementById('message-input');
const messageContainer = document.getElementById('message-container');
appendMessage('Chat App started');

var socket = new WebSocket('ws://' + window.location.host + '/ws');

function appendMessage(message) {
    const messageElement = document.createElement('div')
    messageElement.innerText = message
    messageContainer.append(messageElement)
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
    appendMessage(event.data)
};

messageForm.addEventListener('submit', e => {
    e.preventDefault()
    const message = messageInput.value
    appendMessage(`You: ${message}`)
    socket.send(message);
    messageInput.value = ''
})

