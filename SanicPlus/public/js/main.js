const menu = document.getElementById('menu');
const hamburgerMenu = document.getElementById('hamburger-menu');
const socialIcons = document.getElementById('social-icons');
const footerSocialIcons = document.getElementById('footer-social-icons');

function toggleMenu() {
  menu.classList.toggle('menu--open');
  /* If menu is open, remove the padding-top from body */
  if (menu.classList.contains('menu--open')) {
    document.body.style.paddingTop = '40px';
  } else {
    document.body.style.paddingTop = '420px';
  }
}

function checkScreenSize() {
  if (window.innerWidth >= 576) {
    document.body.style.paddingTop = '0px';
    hamburgerMenu.style.display = 'none';
    socialIcons.style.display = 'flex';
    footerSocialIcons.style.display = 'none';
    menu.classList.remove('menu--open');
  } else {
    hamburgerMenu.style.display = 'flex';
    socialIcons.style.display = 'none';
    footerSocialIcons.style.display = 'flex';
    document.body.style.paddingTop = '420px';
  }
}

window.addEventListener('resize', checkScreenSize);
hamburgerMenu.addEventListener('click', toggleMenu);
document.addEventListener('DOMContentLoaded', checkScreenSize);
