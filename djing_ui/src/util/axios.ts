import axios, { AxiosRequestConfig } from 'axios'
import isNil from 'lodash/isNil'

export const setupAxios = (options?: AxiosRequestConfig) => {
  const instance = axios.create(options)

  instance.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'

  const token = document.head.querySelector('meta[name="csrf-token"]')?.textContent

  instance.defaults.headers.common['X-CSRF-TOKEN'] = token

  instance.interceptors.response.use(
    response => response,
    error => {
      if (axios.isCancel(error)) {
        return Promise.reject(error)
      }

      const response = error.response
      const {
        status,
        data: { redirect },
      } = response

      // Show the user a 500 error
      if (status >= 500) {
        Djing.$emit('error', error.response.data.message)
      }

      // Handle Session Timeouts (Unauthorized)
      if (status === 401) {
        // Use redirect if being specificed by the response
        if (!isNil(redirect)) {
          location.href = redirect
          return
        }

        Djing.redirectToLogin()
      }

      // Handle Forbidden
      if (status === 403) {
        Djing.visit('/403')
      }

      // Handle Token Timeouts
      if (status === 419) {
        Djing.$emit('token-expired')
      }

      return Promise.reject(error)
    }
  )

  return instance
}
