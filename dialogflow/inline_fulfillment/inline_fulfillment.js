'use strict';

const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const admin = require('firebase-admin');

admin.initializeApp();

const db = admin.firestore();

process.env.DEBUG = 'dialogflow:debug';

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  	const agent = new WebhookClient({ request, response });
  	const elements = agent.session.split('/');
    const lastElement = elements[elements.length - 1];
    const ref = db.collection('users').doc(lastElement);
  
    function getCourier(agent) {
    	const courier = agent.parameters.courier;
    	return ref.set({Courier: courier});
    }
  
    function getLocation(agent) {
    	const location = agent.parameters.location;
    	return ref.update({Location: location});
    }
  
    function getLocationType(agent) {
    	const locationType = agent.parameters.locationType;
    	return ref.update({LocationType: locationType});
    }
  
  	function getTime(agent) {
    	const time = agent.parameters.time;
    	return ref.update({Time: time});
    }
  
    function getFlexibility(agent) {
    	const positive = agent.parameters.positive;

      	if (positive == 'Yes') {
          return ref.update({Flexibility: "Negative"});
        } else {
          return ref.update({Flexibility: "Positive"});
        }
    }
  
 	function getReliability(agent) {
    	const positive = agent.parameters.positive;

      	if (positive == 'Yes') {
          return ref.update({Reliability: "Positive"});
        } else {
          return ref.update({Reliability: "Negative"});
        }
    }

 	function getStandardization(agent) {
    	const positive = agent.parameters.positive;
          
      	if (positive == 'Yes') {
          return ref.update({Standardization: "Positive"});
        } else {
          return ref.update({Standardization: "Negative"});
        }
    }

 	function getAttitude(agent) {
    	const positive = agent.parameters.positive;

      	if (positive == 'Yes') {
          return ref.update({Attitude: "Positive"});
        } else if (negative == 'No') {
          return ref.update({Attitude: "Negative"});
        }
    }
  
 	function getFeedback(agent) {
    	const feedback = agent.query;
    	return ref.update({Feedback: feedback});
    }
                                                                  
    let intentMap = new Map();

    intentMap.set('courier', getCourier);
    intentMap.set('location', getLocation);
    intentMap.set('location-type', getLocationType);
  	intentMap.set('time', getTime);
  	intentMap.set('flexibility - yes', getFlexibility);
  	intentMap.set('flexibility - no', getFlexibility);
  	intentMap.set('reliability - yes', getReliability);
    intentMap.set('reliability - no', getReliability);
    intentMap.set('standardization - yes', getStandardization);
  	intentMap.set('standardization - no', getStandardization);
    intentMap.set('attitude - yes', getAttitude);
  	intentMap.set('attitude - no', getAttitude);
  	intentMap.set('overall-feedback', getFeedback);

    agent.handleRequest(intentMap);
});