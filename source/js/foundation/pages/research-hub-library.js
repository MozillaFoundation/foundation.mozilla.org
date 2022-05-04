function main() {
  console.log("Hello World");
  const filterSection = document.getElementById("filter")
  filterSection.classList.add("tw-hidden")

  const filterJumpLink = document.getElementById("filter-section-jump-link")
  filterJumpLink.classList.add("tw-hidden")

  const filterShowButton = document.getElementById("filter-section-show-button")
  filterShowButton.classList.remove("tw-hidden")
}

main()
