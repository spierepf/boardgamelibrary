export function bggId(itemElement) {
  return itemElement.getAttribute('id')
}

export function primaryName(itemElement) {
  let retval = null;
  Array.prototype.slice.call(itemElement.getElementsByTagName("name")).forEach(nameElement => {
    if (retval === null || nameElement.getAttribute('type') === 'primary') {
      retval = nameElement.getAttribute('value')
    }
  })
  return retval;
}

export function yearPublished(itemElement) {
  const yearpublishedElements = itemElement.getElementsByTagName("yearpublished")
  return (yearpublishedElements.length > 0) ? yearpublishedElements[0].getAttribute("value") : null
}

export function displayName(itemElement) {
  const _primaryName = primaryName(itemElement)
  const _yearPublished = yearPublished(itemElement)
  return _yearPublished === null ? _primaryName : `${_primaryName} (${_yearPublished})`
}

export function createItemWithPrimaryName(primaryName) {
  return new window.DOMParser().parseFromString("<item id='none' type='boardgame'><name type='primary' value='" + primaryName + "'/></item>", 'text/xml').documentElement
}

async function bggBaseUrl() {
  return "https://boardgamegeek.com"
  // if (sessionStorage.bggBaseUrl) {
  //     return sessionStorage.bggBaseUrl
  // } else if (process.env.BGG_BASE_URL) {
  //     sessionStorage.bggBaseUrl = process.env.BGG_BASE_URL
  //     return sessionStorage.bggBaseUrl
  // } else {
  //     return fetch(`${process.env.VUE_APP_SERVER_URL}/clientConfiguration`)
  //         .then(response => response.json())
  //         .then(json => sessionStorage.bggBaseUrl = json.BGG_BASE_URL)
  // }
}

export async function searchBgg(searchInput) {
  return await bggBaseUrl()
    .then(bggBaseUrl => fetch(bggBaseUrl + '/xmlapi2/search?type=boardgame,boardgameaccessory,boardgameexpansion&query=' + encodeURIComponent(searchInput.replace(/\s/g, '+')) + ''))
    .then(response => response.text())
    .then(text =>
      Array.prototype.slice.call(new window.DOMParser().parseFromString(text, 'text/xml').documentElement.getElementsByTagName('item'))
    )
}
