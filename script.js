var hist = '';

function getDateTime()
{
  var date = new Date();
  var dt = date.toDateString() + " " + date.toLocaleTimeString();
  return dt
}

function chat(){

  // var apigClient = apigClientFactory.newClient();

  var msg = document.getElementById("txt").value;
  hist = hist + getDateTime() + "  YOU:  " + msg + '\n';
  document.getElementById("txt").value = "";
  document.getElementById("textarea").value = hist;

  // var apigClient = apigClientFactory.newClient({
  //   accessKey: 'ACCESS_KEY',
  //   secretKey: 'SECRET_KEY',
  // });
  //
  var apigClient = apigClientFactory.newClient({
    //apiKey: 'rm6GCnF8P55SEmEiqYT682hpRJMOX5oAa1TvJcTU'
  });

  var params = {
    // This is where any modeled request parameters should be added.
    // The key is the parameter name, as it is defined in the API in API Gateway.
    param0: '',
    param1: ''
  };

  var body = {
    "messages": msg // This is where you define the body of the request,
  };

  var additionalParams = {
    // If there are any unmodeled query parameters or headers that must be
    //   sent with the request, add them here.
    headers: {
      'Access-Control-Allow-Origin':'*'
    },
    queryParams: {
      param0: '',
      param1: ''
    }
  };


  apigClient.chatbotPost(params, body)
      .then(function(result){
        hist = hist + getDateTime() + "  BOT:  " + result.data.message + '\n';
        document.getElementById("textarea").value = hist;
        // Add success callback code here.
      }).catch( function(result){
        console.log(result.data.message);
        // Add error callback code here.
      });

}
