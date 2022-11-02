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
    forms.forEach(form => form.style.display = 'none');
    
    fetch(`/posts`)
    .then(response => response.json())
    .then(posts => { 
        posts.forEach(post => show_edit(post));
        posts.forEach(post => likes(post));
        posts.forEach(post => unlike(post));
        posts.forEach(post => flagging(post))
    }
    )
});

function flagging(post)
{
    flag = document.querySelector(`.flag[data-index="${post.id}"]`);
    if(flag)
        flag = flag.innerHTML;
        console.log(flag);
        if (flag == "liked")
        {
            document.querySelector(`#unlike[data-index="${post.id}"]`).style.display = 'block';
            document.querySelector(`#like[data-index="${post.id}"]`).style.display = 'none';
        }
        else if(flag == "not_liked")
        {
            document.querySelector(`#unlike[data-index="${post.id}"]`).style.display = 'none';
            document.querySelector(`#like[data-index="${post.id}"]`).style.display = 'block';
        }
}


function likes(post)
{
    
    like_button = document.querySelector(`#like[data-index="${post.id}"]`);
    if(like_button)
    {
        like_button.addEventListener('click',add_like);
        like_button.myParam = post;
    }
}

function unlike(post)
{
    if (post.likes > 0)
    {   

        unlike_button = document.querySelector(`#unlike[data-index="${post.id}"]`);
        if(unlike_button)
        {
            unlike_button.addEventListener('click',remove_like);
            unlike_button.myParam = post;
        }
    }
  
}


function remove_like(evt)
{
    console.log(`trying to delete`);
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    post = evt.currentTarget.myParam;


    const request2 = new Request(
        `/unlike/${post.id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
        fetch(request2, {
            method: 'DELETE',
            body: JSON.stringify({
                liker: user_id,
            })
        })
        .then(() => 
            fetch(`/post/${post.id}`)
            .then(response => response.json())
            .then(post => {
                document.querySelector(`span[data-index = "${post.id}"]`).innerHTML = post.likes;
                document.querySelector(`#unlike[data-index="${post.id}"]`).style.display = 'none';
                document.querySelector(`#like[data-index="${post.id}"]`).style.display = 'block';

            })

        )

    
    evt.preventDefault();
}


function add_like(evt)
{
    console.log("trying to like");
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    post = evt.currentTarget.myParam;
    
    console.log(user_id);


    const request2 = new Request(
        `/like/${post.id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

        fetch(request2, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
            liker: user_id,
            })
        })
        .then(() =>
            fetch(`/post/${post.id}`)
            .then(response => response.json())
            .then(post => {
                document.querySelector(`span[data-index = "${post.id}"]`).innerHTML = post.likes;
                document.querySelector(`#unlike[data-index="${post.id}"]`).style.display = 'block';
                document.querySelector(`#like[data-index="${post.id}"]`).style.display = 'none';

            })
        )

    evt.preventDefault();
}

function show_edit(post)
{
    button =  document.getElementById(`${post.id}`);
    if(button)
    {
        button.addEventListener('click',save);
        button.myParam = post;
    }
}

function save(evt)
{

    post = evt.currentTarget.myParam;
    document.getElementById(`body${post.id}`).style.display = 'none';
    document.getElementById(`new_body${post.id}`).style.display = 'block';
    document.getElementById(`compose_body${post.id}`).innerHTML = post.body;
    this.style.display = 'none';
    save_button = document.getElementById(`save${post.id}`);
    save_button.addEventListener('click',saving);
    save_button.myParam = post;
    
}
    
function saving(evt)
    
{
        
    post = evt.currentTarget.myParam;
    new_body = document.querySelector(`#compose_body${post.id}`).value;
    console.log(`new body: ${new_body}`);

    const request = new Request(
        `/post/${post.id}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
        
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            body: new_body
        })
    })
    body = document.getElementById(`body${post.id}`);
    body.style.display = 'block';
    body.innerHTML = new_body;
    document.getElementById(`new_body${post.id}`).style.display = 'none';
    document.getElementById(`${post.id}`).style.display = 'block';
    evt.preventDefault();
}