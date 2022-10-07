function main(){
  console.log('Hello World')
  switchFromPaginationToLoadMore()
}

function switchFromPaginationToLoadMore(){
  const loadMore = document.getElementById('load-more')
  loadMore.classList.remove('tw-hidden')

  const pagination = document.getElementById('pagination')
  pagination.classList.add('tw-hidden')
}

main()
