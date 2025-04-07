const request_user = JSON.parse(document.getElementById('user_id').textContent);
const container = document.querySelector('#grail-list');
const csrftoken = getCookie('csrftoken');
const item_cards = document.querySelectorAll('.grail-item');
const search_box = document.querySelector('#search-box');

populateFilters(item_cards);
search_box.addEventListener('keyup', filterItems);

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
        //Get our response (boolean with new checkbox state)
        const data = await response.json();
        //Change the checkbox on the page based on its new state.

        if(data.response == true) {
            document.getElementById(item_name).checked = true
        }
        else {
            document.getElementById(item_name).checked = false
        }
    }
});

//performs a regex search on each items metadata, only showing matches.
function filterItems(e){
    let filter = new RegExp(e.target.value, 'i');
    item_cards.forEach((element) => {
        element.classList.toggle('hidden', filter !== '' && !(filter.test(element.getAttribute('name')) || filter.test(element.getAttribute('base')) || filter.test(element.getAttribute('rarity'))))
    })
};

//uses preset quick filters e.g. "One-handed Axe".
function quickFilter(e){
    let type = e.target.innerText;
    if(type !== "All Items"){
        item_cards.forEach((element) => {
            element.classList.toggle('hidden', !(element.getAttribute('base') == type || element.getAttribute('rarity') == type))
        })
    }
    else{
        item_cards.forEach((element) => {
            element.classList.toggle('hidden', false)
        }) 
    }
}

//Creates a list of unique bases... While its unlikely new bases will be added this adds some future proofing to our html.
function populateFilters(item_list){
    var bases = new Set();

    item_list.forEach((element) => {
        bases.add(element.getAttribute('base'));
    })

    let filter_div = document.getElementById('item-bases');

    //Add the reset button.
    const filter_item = document.createElement("a");
    filter_item.innerText = "All Items";
    filter_item.className = "filter-list";
    filter_item.href = "#"
    filter_item.addEventListener('click', quickFilter);
    filter_div.appendChild(filter_item);
    
    //Add each base to the list of filter options
    bases.forEach((element) => {
        const filter_item = document.createElement("a");
        filter_item.innerText = element;
        filter_item.className = "filter-list";
        filter_item.href = "#"
        filter_item.addEventListener('click', quickFilter);
        filter_div.appendChild(filter_item);
    })
    
}
//Gets the CSRF token.
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
