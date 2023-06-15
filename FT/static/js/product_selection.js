
/* function test(e) {
    console.log("click")
  }


checkBoxes = document.querySelectorAll("li");

checkBoxes.forEach(element => {
    form = element.querySelector("#product_id");
    console.log(form)
    product_id = element.querySelector(".nrf");
    console.log(product_id)
    form.value = "we"
    console.log(form)
    element.addEventListener("click", test);
}); */


function add_entry(id, url, apartment, room, slug) {
  console.log("ADD")
  console.log("ID", id)
  console.log("URL", url)
  console.log("APARTMENT", apartment)
  console.log("ROOM", room)
  console.log("SLUG", slug)
  const addedList = document.getElementById("chosen_list");
  const avaliableList = document.getElementById("avaliable_list");
  const entry = {
    add: true,
    id: id
  }
  fetch(`${url}/collections/${apartment}/${room}/${slug}`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "Content-Type": "application/json"
    })
  })
  .then(() => {
    fetch(`/process-list/${apartment}/${room}/${slug}/${id}/add`, {
      method: "GET"
    })
    .then(response => {
      return response.text();
    })
    .then(html => {
      addedList.innerHTML = html;
    })
  })
  .then(() => {
    fetch(`/process-list/${apartment}/${room}/${slug}/${id}/remove`, {
      method: "GET"
    })
    .then(response => {
      return response.text();
    })
    .then(html => {
      avaliableList.innerHTML = html;
    })
  })
}

function remove_entry(id, url, apartment, room, slug) {
  console.log("REMOVE")
  console.log("ID", id)
  console.log("URL", url)
  console.log("APARTMENT", apartment)
  console.log("ROOM", room)
  console.log("SLUG", slug)
  const addedList = document.getElementById("chosen_list");
  const avaliableList = document.getElementById("avaliable_list");
  const entry = {
    add: false,
    id: id
  }
  fetch(`${url}/collections/${apartment}/${room}/${slug}`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "Content-Type": "application/json"
    })
  })
  .then(() => {
    fetch(`/process-list/${apartment}/${room}/${slug}/${id}/remove`, {
      method: "GET"
    })
    .then(response => {
      return response.text();
    })
    .then(html => {
      avaliableList.innerHTML = html;
    })
  })
  .then(() => {
    fetch(`/process-list/${apartment}/${room}/${slug}/${id}/add`, {
      method: "GET"
    })
    .then(response => {
      return response.text();
    })
    .then(html => {
      addedList.innerHTML = html;
    })
  })
}