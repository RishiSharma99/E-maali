'use strict';

console.log("Started");

const applicationServerPublicKey = 'BOwpInymOBNQaJkZS7pUEkY2nmQDyRpIF4JFt_lWwna3EHlUExsQ8Ye_W2-4PI8GMJxWIpeZjkz_cxnBC3gs03c';

const logoutButton = document.querySelector('.js-logout-btn');
const logoutButton = document.querySelector('.js-subscribe-btn');

let isSubscribed = false;
let swRegistration = null;

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}
if ('serviceWorker' in navigator && 'PushManager' in window){
  console.log('Service Worker and Push is supported');

  navigator.serviceWorker.register('static/sw.js')
    .then(function(swReg){
      console.log('Service Worker is registered' , swReg);

      swRegistration = swReg;
      initailizeUI();
      subscribeUser();
    })
    .catch(function(error){
      console.error('Service Worker error' , error);
    });
} else {
  console.warn('Push messaging is not Supported');
  pushButton.textContent = 'Push Not Supported';
}

function initailizeUI() {
  subscribeUser();

  logoutButton.addEventListener('click' , function() {
    console.log("unsubscribing");
    
    logoutButton.disabled = true;

    unsubscribeUser();
    console.log('unsubscribed');
    window.location.replace('/clear-session');
  });

  swRegistration.pushManager.getSubscription()
  .then(function(subscription){
    isSubscribed = !(subscription == null);

    updateSubscriptionOnServer(subscription);

    if (isSubscribed){
      console.log('User IS subscribed');
    } else {
      console.log('User is NOT subscribed');
    }

  });
}

function subscribeUser() {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  swRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  })
  .then(function(subscription) {
    console.log('User is subscribed.');

    updateSubscriptionOnServer(subscription);

    isSubscribed = true;
  })
  .catch(function(err) {
    console.log('Failed to subscribe the user: ', err);
  });
}

function updateSubscriptionOnServer(subscription) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST' , "/subscribe");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.onreadystatechange = function(){
    console.log("Response Code:"  , xhr.status);
  };
  if (subscription==null){
    xhr.send(JSON.stringify({}));  
  } else {
    xhr.send(JSON.stringify(subscription));
  }
  
  const subscriptionJson = document.querySelector('.js-subscription-json');

  if (subscription) {
    console.log(JSON.stringify(subscription));
  } else {
    console.log("NOOOO");
  }
}

function unsubscribeUser() {
  console.log("unsubscribing");
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    if (subscription) {
      return subscription.unsubscribe();
    }
  })
  .catch(function(error) {
    console.log('Error unsubscribing', error);
  })
  .then(function() {
    updateSubscriptionOnServer(null);

    console.log('User is unsubscribed.');
    isSubscribed = false;

  });
}