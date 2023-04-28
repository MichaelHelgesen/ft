console.log("hello world")

function test(e) {
    console.log("click")
  }


checkBoxes = document.querySelectorAll("li");

checkBoxes.forEach(element => {
    form = element.querySelector("#product_id");
    console.log(form)
    product_id = element.querySelector(".nrf");
    console.log(product_id)
    //form.value = "we"
    //console.log(form)
    //element.addEventListener("click", test);
});
