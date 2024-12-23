export const minimum = (original_promise: any, delay: number = 100) => {
  return Promise.all([
    original_promise,
    new Promise((resolve: any) => setTimeout(resolve(), delay))
  ]).then(result => result[0])
}