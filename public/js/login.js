import * as firebase from "https://www.gstatic.com/firebasejs/9.3.2/firebase.js";

// Initialize Firebase
const firebaseConfig = {
  apiKey: "AIzaSyAnnLDZAy1D8I6bG-JrL1yw4ocM9Dz2sUE",
  authDomain: "jameshall-ninja-387911.firebaseapp.com",
};
firebase.initializeApp(firebaseConfig);

// Initialize the FirebaseUI Widget using Firebase.
const ui = new firebaseui.auth.AuthUI(firebase.auth());

// Sign in with Google using the redirect method
const signInWithGoogle = async () => {
  const provider = new firebase.auth.GoogleAuthProvider();
  const result = await ui.signInWithRedirect(provider);

  // Check the response status code
  const statusCode = result.status;
  if (statusCode === 200) {
    // The user has been signed in successfully.
    const user = result.user;

    // Redirect the user to the home page.
    window.location.href = "/";
  } else {
    // Handle Errors here.
    const errorMessage = await result.error.text();
    throw new Error(errorMessage);
  }
};

// Listen for the signInSuccess event
firebase.auth().onAuthStateChanged(async (user) => {
  if (user) {
    // The user is signed in.
    console.log("User signed in:", user);
  } else {
    // The user is not signed in.
    console.log("User signed out");
  }
});

// Call the signInWithGoogle() function
signInWithGoogle();

