export function fetchFromServer(path, options = null) {
  return fetch(`http://localhost:8000${path}`, options)
}
