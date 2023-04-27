console.log("hello world")

function test() {
    console.log("click")
  }


checkBoxes = document.querySelectorAll("li");

checkBoxes.forEach(element => {
    element.addEventListener("click", test)
});
