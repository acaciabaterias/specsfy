export default function Example() {
  return (
    <div className="bg-white">
      <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8 lg:py-16">
        <div className="rounded-lg bg-indigo-700 px-6 py-6 md:px-12 md:py-12 lg:px-16 lg:py-16 xl:flex xl:items-center">
          <div className="xl:w-0 xl:flex-1">
            <h2 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">Want product news and updates?</h2>
            <p className="mt-3 max-w-3xl text-lg/6 text-indigo-200">Sign up for our newsletter to stay up to date.</p>
          </div>
          <div className="mt-8 sm:w-full sm:max-w-md xl:mt-0 xl:ml-8">
            <form className="sm:flex">
              <input
                id="email-address"
                name="email-address"
                type="email"
                required
                placeholder="Enter your email"
                autoComplete="email"
                aria-label="Email address"
                className="w-full rounded-md px-5 py-3 placeholder-gray-500 outline-hidden focus:outline-2 focus:outline-offset-2 focus:outline-white"
              />
              <button
                type="submit"
                className="mt-3 flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-500 px-5 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-400 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-700 focus:outline-hidden sm:mt-0 sm:ml-3 sm:w-auto sm:shrink-0"
              >
                Notify me
              </button>
            </form>
            <p className="mt-3 text-sm text-indigo-200">
              We care about the protection of your data. Read our{' '}
              <a href="#" className="font-medium text-white underline">
                Privacy Policy.
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
