function getCookie(name) {
   var cookieValue = null;
   if (document.cookie && document.cookie != '') {
     var cookies = document.cookie.split(';');
     for (var i = 0; i < cookies.length; i++) {
       var cookie = jQuery.trim(cookies[i]);
       if (cookie.substring(0, name.length + 1) == (name + '=')) {
         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
         break;
       }
     }
   }
   return cookieValue;
}

async function likeAPI(id){
    let response = await fetch('/like', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({"id":id})
    });
    let result = await response.json();
}

function ChangeCount(id,change_by){
    if(is_authenticated){
        count_element = document.getElementById("like-count-"+id)
        count_element.innerHTML = parseInt(count_element.innerText) + change_by + " likes"
    }
}

function HandleToggle(first_class, second_class, id){
    if(is_authenticated){
        visible_element = document.getElementById(first_class);
        visible_element.style.display = 'none';
        fake_element=document.getElementById(second_class);
        fake_element.style.display = 'flex';
        likeAPI(id);
    }else{
        window.location.href="/login"
    }
}

function action(event, id, type, action){
    event.preventDefault();
    if (type=="actual"){
        if(action==="liked"){
            HandleToggle("actual-action-"+id,"fake-like-action-"+id, id);
            ChangeCount(id, -1);
        }else{
            HandleToggle("actual-action-"+id,"fake-liked-action-"+id, id );
            ChangeCount(id, +1);
        }
    }
    else{
        if(action==="liked"){
            HandleToggle("fake-liked-action-"+id,"fake-like-action-"+id, id );
            ChangeCount(id, -1)
        }
        else{
            HandleToggle("fake-like-action-"+id,"fake-liked-action-"+id, id );
            ChangeCount(id, +1)
        }
    }
}