export function fetchFromServer(path, options = null) {
  let url = path.startsWith('http') ? path : `http://localhost:8000${path}`
  return fetch(url, options).then((response) => {
    if (response.ok) {
      return response.json()
    } else {
      console.log(options)
      console.log(response)
      let error = new Error(response.statusText)
      error.response = response
      throw error
    }
  })
}

export function urlFor(datatype, id = null) {
  return `http://localhost:8000/api/library/${datatype}/` + (id ? `${id}/` : '')
}

export function urlForQuery(datatype, key, value) {
  return `http://localhost:8000/api/library/${datatype}/?${key}=${value}`
}
