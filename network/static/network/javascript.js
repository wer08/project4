function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded',function(){
    forms = document.querySelectorAll('.new_body');
    console.log(forms);
    forms.forEach(form => form.style.display = 'none');

    fetch(`posts`)
    .then(response => response.json())
    .then(posts => {
    // ... do something else with emails ...
        posts.forEach(post => show_edit(post));
  }
  )
});
function show_edit(post)
{
    button = document.getElementById(`${post.id}`);
    
    button.addEventListener('click',function(){
        document.getElementById(`body${post.id}`).style.display = 'none';
        document.getElementById(`new_body${post.id}`).style.display = 'block';
        document.getElementById(`compose_body${post.id}`).innerHTML = post.body;
        button.style.display = 'none';
        document.getElementById(`save${post.id}`).addEventListener('click',edit(post));
    });
    
}

function edit(post)
{
    new_body = document.querySelector(`#compose_body${post.id}`).value;
    console.log("blabla");
    const request = new Request(
        `/posts/${post.id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            body: new_body
        })
      })
      .then(function(){
        document.getElementById(`body${post.id}`).style.display = 'block';
        document.getElementById(`new_body${post.id}`).style.display = 'none';
      })
}