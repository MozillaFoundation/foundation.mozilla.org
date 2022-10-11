import 'htmx.org'

function main(){
  htmx.onLoad(() => {
    switchFromPaginationToLoadMore()
    disableLoadMoreButtonOnRequest()
  })
}

function switchFromPaginationToLoadMore(){
  const loadMore = document.getElementById('load-more')
  loadMore.classList.remove('tw-hidden')

  const pagination = document.getElementById('pagination')
  pagination.classList.add('tw-hidden')
}

function disableLoadMoreButtonOnRequest() {
  // Disable the load more button when the request is triggered.
  // This is a signal to the user an prevents duplicate triggering.
  // We don't need to reactivate the button because it is replaced with the response.
  const loadMore = document.getElementById('load-more')
  const loadMoreButton = loadMore.getElementsByTagName('button')[0]
  loadMoreButton.addEventListener('htmx:beforeRequest', (event) => {
    event.target.setAttribute('disabled', '')
  })
}

main()
