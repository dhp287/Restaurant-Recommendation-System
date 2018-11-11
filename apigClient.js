/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

var apigClientFactory = {};

// var data = {
//         UserPoolId : 'us-east-1_iUNvFj1uo', // Your user pool id here
//         ClientId : '142o33rei8etvg1hkji62rndi0' // Your client id here
//     };
//     var userPool = new AmazonCognitoIdentity.CognitoUserPool(data);
// var cognitoUser = userPool.getCurrentUser();
//
// if (cognitoUser != null) {
//     cognitoUser.getSession(function(err, result) {
//         if (result) {
//             console.log('You are now logged in.');
//
//             // Add the User's Id Token to the Cognito credentials login map.
//             AWS.config.credentials = new AWS.CognitoIdentityCredentials({
//                 IdentityPoolId: 'us-east-1:84ca9203-7982-41f3-ba12-b70a8020cd03',
//                 Logins: {
//                     'cognito-idp.us-east-1.amazonaws.com/us-east-1_iUNvFj1uo': result.getIdToken().getJwtToken()
//                 }
//             });
//         }
//     });
// }
// //call refresh method in order to authenticate user and get new temp credentials
// AWS.config.credentials.refresh((error) => {
//     if (error) {
//         console.error(error);
//     } else {
//         console.log('Successfully logged!');
//     }
//     });


var url = window.location.href;
url = url.split('#')[1];
var arr = url.split('&');
var token = arr[0].split('=')[1];


AWS.config.region = 'us-east-1';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId : 'us-east-1:84ca9203-7982-41f3-ba12-b70a8020cd03', // your identity pool id here
    Logins : {
        // Change the key below according to the specific region your user pool is in.
        'cognito-idp.us-east-1.amazonaws.com/us-east-1_iUNvFj1uo' : token
    }
});

AWS.config.credentials.refresh((error) => {
    if (error) {
        console.error(error);
    } else {
        console.log('Successfully logged!');
    }
});


apigClientFactory.newClient = function (config) {
    var apigClient = { };
    if(config === undefined) {
        config = {
            accessKey: '',
            secretKey: '',
            sessionToken: '',
            region: '',
            apiKey: undefined,
            defaultContentType: 'application/json',
            defaultAcceptType: 'application/json'
        };
    }
    if(config.accessKey === undefined) {
        config.accessKey = AWS.config.credentials.accessKeyId;
    }
    if(config.secretKey === undefined) {
        config.secretKey = AWS.config.credentials.secretAccessKey;
    }
    if(config.apiKey === undefined) {
        config.apiKey = '';
    }
    if(config.sessionToken === undefined) {
        config.sessionToken = AWS.config.credentials.sessionToken;
    }
    if(config.region === undefined) {
        config.region = 'us-east-1';
    }
    //If defaultContentType is not defined then default to application/json
    if(config.defaultContentType === undefined) {
        config.defaultContentType = 'application/json';
    }
    //If defaultAcceptType is not defined then default to application/json
    if(config.defaultAcceptType === undefined) {
        config.defaultAcceptType = 'application/json';
    }


    // extract endpoint and path from url
    var invokeUrl = 'https://znirkpc8x5.execute-api.us-east-1.amazonaws.com/beta';
    var endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
    var pathComponent = invokeUrl.substring(endpoint.length);

    var sigV4ClientConfig = {
        accessKey: config.accessKey,
        secretKey: config.secretKey,
        sessionToken: config.sessionToken,
        serviceName: 'execute-api',
        region: config.region,
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var authType = 'NONE';
    if (sigV4ClientConfig.accessKey !== undefined && sigV4ClientConfig.accessKey !== '' && sigV4ClientConfig.secretKey !== undefined && sigV4ClientConfig.secretKey !== '') {
        authType = 'AWS_IAM';
    }

    var simpleHttpClientConfig = {
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var apiGatewayClient = apiGateway.core.apiGatewayClientFactory.newClient(simpleHttpClientConfig, sigV4ClientConfig);



    apigClient.chatbotPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }

        apiGateway.core.utils.assertParametersDefined(params, ['body'], ['body']);

        var chatbotPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/chatbot').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };


        return apiGatewayClient.makeRequest(chatbotPostRequest, authType, additionalParams, config.apiKey);
    };


    apigClient.chatbotOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }

        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);

        var chatbotOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/chatbot').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };


        return apiGatewayClient.makeRequest(chatbotOptionsRequest, authType, additionalParams, config.apiKey);
    };


    return apigClient;
};
