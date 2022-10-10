import 'htmx.org'

function main(){
  htmx.onLoad(() => switchFromPaginationToLoadMore())
}

function switchFromPaginationToLoadMore(){
  const loadMore = document.getElementById('load-more')
  loadMore.classList.remove('tw-hidden')

  const pagination = document.getElementById('pagination')
  pagination.classList.add('tw-hidden')
}

main()
