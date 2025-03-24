const request_user = JSON.parse(document.getElementById('user_id').textContent);
const container = document.querySelector('#grail-list');
const csrftoken = getCookie('csrftoken');

//Dynamically listens for clicks on each item, and flips the item's hasfound field
container.addEventListener('click', async function(e) {
    if(e.target.classList.contains('grail-item')) {
        //Get the name of the item we want
        var item_name = e.target.getAttribute("name");
        //Make the request and update the grail status on the db
        const response = await fetch("update_grail", {
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            method: "POST",
            body: JSON.stringify({item:item_name})
        });
        console.log(response.status)
    }
});

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
