// Connect to the Socket.IO server
const socket = io('http://localhost:5000', { transport: 'websocket' });  // Replace with your server URL

// Emit a chat request event
socket.emit('chat_request', { from_id: 'user1', to_id: 'user2' });

// Listen for a chat request event
socket.on('chat_request', (data) => {
  console.log('Chat request received:', data);
});

// Emit an accept request event
socket.emit('accept_request', { from_id: 'user2', to_id: 'user1' });
// Listen for a chat accepted event
socket.on('chat_accepted', (data) => {
  console.log('Chat accepted:', data);

  const message = { message: 'Hello, how are you?', room: data.room };
  socket.emit('message', message);
});

// Listen for a message event
socket.on('message', (data) => {
  console.log('Message received:', data);
  // Display the message in your chat interface (e.g., append to #chat div)
  document.getElementById('chat').innerHTML += `<p>${data.message}</p>`;
});
