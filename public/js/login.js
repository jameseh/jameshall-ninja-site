import { getAuth, getRedirectResult, GoogleAuthProvider } from "firebase/auth";
import { initializeApp } from 'firebase/app';

const firebaseConfig = {
  apiKey: "AIzaSyAnnLDZAy1D8I6bG-JrL1yw4ocM9Dz2sUE",
  authDomain: "jameshall-ninja-387911.firebaseapp.com",
};

const app = initializeApp(firebaseConfig);

var uiConfig = {
  callbacks: {
    signInSuccessWithAuthResult: function(authResult, redirectUrl) {
      return true;
    },
    uiShown: function() {
      document.getElementById('loader').style.display = 'none';
    }
  },
  signInFlow: 'redirect',
  signInSuccessUrl: '/dashboard',
  signInOptions: [
    firebase.auth.GoogleAuthProvider.PROVIDER_ID,
  ],
  tosUrl: '/tos',
  privacyPolicyUrl: '/pp'
};

ui.start('#firebaseui-auth-container', {
  signInOptions: [
    // List of OAuth providers supported.
    firebase.auth.GoogleAuthProvider.PROVIDER_ID,
  ],
});

// Initialize the FirebaseUI Widget using Firebase.
var ui = new firebaseui.auth.AuthUI(firebase.auth());

const auth = getAuth();
const provider = new GoogleAuthProvider();

async function signInWithGoogle() {
  // Sign in with Google using the redirect method
  await signInWithRedirect(auth, provider);

  // Check the response status code
  const statusCode = response.status;
  if (statusCode === 200) {
    // Get the redirect result
    const result = await getRedirectResult(auth);

    // This gives you a Google Access Token. You can use it to access Google APIs.
    const credential = provider.credentialFromResult(result);
    const token = credential.accessToken;

    // The signed-in user info.
    const user = auth.currentUser;
    // IdP data available using getAdditionalUserInfo(result)
    // ...

    // Get the refresh token.
    const refreshToken = await auth.signInWithCredential(credential).refreshToken;

    // Encrypt the refresh token before storing it in the cookie.
    const encryptedRefreshToken = encrypt(refreshToken);

    // Set the refresh token expiration time to 1 day.
    auth.setRefreshToken(encryptedRefreshToken, 1000 * 60 * 60 * 24);

    // Get the user email, username, and profile pic.
    const email = user.email;
    const name = user.displayName;
    const profilePicUrl = user.photoURL;
   
    // Create a cookie with the user's email, name, profile pic, and encrypted refresh token.
    const cookie = `email=${email}; user_id=${name}; profilePicUrl=${profilePicUrl}; refreshToken=${encryptedRefreshToken}`;

    // Set the cookie expiration time to 1 hour.
    document.cookie = cookie;

    // Check if there is a refresh token in the cookie.
    const refreshTokenIsValid = document.cookie.match(/refreshToken=(.*?);/)[1];

    // If there is a refresh token, decrypt it.
    if (refreshTokenIsValid) {
      const decryptedRefreshToken = decrypt(refreshTokenIsValid);

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
}
