import * as firebase from 'https://www.gstatic.com/firebasejs/8.0/firebase-app.js';
import * as firebaseAuth from 'https://www.gstatic.com/firebasejs/8.0/firebase-auth.js';

firebase.initializeApp({
  apiKey: "AIzaSyAnnLDZAy1D8I6bG-JrL1yw4ocM9Dz2sUE",
  authDomain: "jameshall-ninja-387911.firebaseapp.com",
});


const auth = firebaseAuth();

// Redirect to Firebase
const redirectUrl = firebase.auth().getRedirectResult().redirectUrl;
const response = await fetch(redirectUrl);

// Check the response status code
const statusCode = response.status;
if (statusCode === 200) {
  // Get the redirect result
  const result = await getRedirectResult(auth);

  // This gives you a Google Access Token. You can use it to access Google APIs.
  const credential = GoogleAuthProvider.credentialFromResult(result);
  const token = credential.accessToken;

  // The signed-in user info.
  const user = result.user;
  // IdP data available using getAdditionalUserInfo(result)
  // ...

  // Get the refresh token.
  const refreshToken = await auth.signInWithCredential(credential).refreshToken;

  // Encrypt the refresh token before storing it in a cookie.
  const encryptedRefreshToken = encrypt(refreshToken);

  // Set the refresh token expiration time.
  auth.setRefreshTokenExpirationTime(refreshToken, 1000 * 60 * 60 * 24); // 1 day

  // Get the user email, username, and profile pic.
  const email = user.email;
  const name = user.displayName;
  const profilePicUrl = user.photoURL;
   
  // Create a cookie with the user's email, name, profile pic, and encrypted refresh token.
  const cookie = `email=${email}; user_id=${name}; profilePicUrl=${profilePicUrl}; refreshToken=${encryptedRefreshtoken}`;

  // Set the cookie expiration time.
  document.cookie = cookie;

  // Check if there is a refresh token in the cookie.
  const refreshToken = document.cookie.match(/refreshToken=(.*?);/)[1];

  // If there is a refresh token, decrypt it.
  if (refreshToken) {
    const decryptedRefreshToken = decrypt(refreshToken);

    // Check the validity of the refresh token.
    if (auth.isRefreshTokenValid(decryptedRefreshToken)) {
      // Sign in the user using the refresh token.
      await auth.signInWithRefreshToken(decryptedRefreshToken);

      // Redirect the user to the home page.
      window.location.href = "/";
    }
  }
} else {
  // Handle Errors here.
  const errorMessage = await response.text();
  throw new Error(errorMessage);
}
