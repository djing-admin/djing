import forEach from 'lodash/forEach'

const __ = (key: any, replace: any) => {
  let translation = Djing.config('translations')[key]
    ? Djing.config('translations')[key]
    : key

  forEach(replace, (value: any, key: any) => {
    key = new String(key)

    if (value === null) {
      console.error(
        `Translation '${translation}' for key '${key}' contains a null replacement.`
      )

      return
    }

    value = new String(value)

    const searches = [
      ':' + key,
      ':' + key.toUpperCase(),
      ':' + key.charAt(0).toUpperCase() + key.slice(1),
    ]

    const replacements = [
      value,
      value.toUpperCase(),
      value.charAt(0).toUpperCase() + value.slice(1),
    ]

    for (let i = searches.length - 1; i >= 0; i--) {
      translation = translation.replace(searches[i], replacements[i])
    }
  })

  return translation
}

export default __