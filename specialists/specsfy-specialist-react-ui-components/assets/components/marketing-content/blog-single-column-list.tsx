const posts = [
  ['Boost your conversion rate', 'Marketing'],
  ['How to use search engine optimization to drive sales', 'Sales'],
  ['Improve your customer experience', 'Business'],
]

export default function Example() {
  return (
    <div className="bg-white py-24 sm:py-32 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl">
          <h2 className="text-4xl font-semibold tracking-tight text-pretty text-gray-900 sm:text-5xl dark:text-white">
            From the blog
          </h2>
          <p className="mt-2 text-lg/8 text-gray-600 dark:text-gray-300">
            Learn how to grow your business with our expert advice.
          </p>
          <div className="mt-10 space-y-16 border-t border-gray-200 pt-10 sm:mt-16 sm:pt-16 dark:border-gray-700">
            {posts.map(([title, category]) => (
              <article key={title} className="flex max-w-xl flex-col items-start">
                <div className="flex items-center gap-x-4 text-xs">
                  <time className="text-gray-500 dark:text-gray-400">Mar 16, 2020</time>
                  <span className="rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 dark:bg-gray-800/60 dark:text-gray-300">
                    {category}
                  </span>
                </div>
                <h3 className="mt-3 text-lg/6 font-semibold text-gray-900 dark:text-white">{title}</h3>
                <p className="mt-5 line-clamp-3 text-sm/6 text-gray-600 dark:text-gray-400">
                  Illo sint voluptas. Error voluptates culpa eligendi.
                </p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
