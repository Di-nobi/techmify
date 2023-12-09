document.addEventListener('DOMContentLoaded', function () {
  var socket = io.connect('http://0.0.0.0:5000');

  function sendChatRequest() {
      var fromId = document.getElementById('fromId').value;
      var toId = document.getElementById('toId').value;

      // Emit 'chat_request' event to the server
      socket.emit('chat_request', { from_id: fromId, to_id: toId });
  }

  function sendLoginRequest() {
      var email = document.getElementById('email').value;
      var password = document.getElementById('password').value;

      // Send a login request using Axios
      axios.post('http://0.0.0.0:5000/sessions', {
          email: email,
          password: password
      })
      .then(function (response) {
          console.log('Login success:', response.data);
      })
      .catch(function (error) {
          console.error('Login error:', error.response.data);
      });
  }

  document.getElementById('sendChatRequestBtn').addEventListener('click', sendChatRequest);
  document.getElementById('loginBtn').addEventListener('click', sendLoginRequest);
});
