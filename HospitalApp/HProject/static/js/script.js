let menu = document.querySelector("#menu-btn");
let navbar = document.querySelector(".navbar");

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () =>
{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}

function toggleDropdown() {
    var dropdownMenu = document.getElementById("myDropdown");
    dropdownMenu.classList.toggle("show");
  }
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropdown-toggle')) {
      var dropdownMenus = document.getElementsByClassName("dropdown-menu");
      for (var i = 0; i < dropdownMenus.length; i++) {
        var openDropdownMenu = dropdownMenus[i];
        if (openDropdownMenu.classList.contains('show')) {
          openDropdownMenu.classList.remove('show');
        }
      }
    }
  };
  function redirect(url) {
    window.location.href = url;
  }

  
  
  

