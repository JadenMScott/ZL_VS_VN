function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
(document).ready(function(){
    setTimeout(function(){
        alert("This is the alert message for timer");
    }, 5000);
})