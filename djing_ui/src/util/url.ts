import identity from 'lodash/identity'
import pickBy from 'lodash/pickBy'

export const url = (base: string, path: string, parameters: any) => {
  let searchParams = new URLSearchParams(pickBy(parameters || {}, identity))

  let queryString = searchParams.toString()

  if (base == '/' && path.startsWith('/')) {
    base = ''
  }

  return base + path + (queryString.length > 0 ? `?${queryString}` : '')
}
