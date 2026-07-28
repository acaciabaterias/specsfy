import { Popover, PopoverButton, PopoverGroup, PopoverPanel } from '@headlessui/react'
import {
  ArrowPathIcon,
  Bars3Icon,
  ChartBarIcon,
  CursorArrowRaysIcon,
  DocumentChartBarIcon,
  ShieldCheckIcon,
  Squares2X2Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { ChevronDownIcon } from '@heroicons/react/20/solid'

const solutions = [
  {
    name: 'Analytics',
    description: 'Get a better understanding of where your traffic is coming from.',
    href: '#',
    icon: ChartBarIcon,
  },
  {
    name: 'Engagement',
    description: 'Speak directly to your customers in a more meaningful way.',
    href: '#',
    icon: CursorArrowRaysIcon,
  },
  { name: 'Security', description: 'Your customers data will be safe and secure.', href: '#', icon: ShieldCheckIcon },
  {
    name: 'Integrations',
    description: "Connect with third-party tools that you're already using.",
    href: '#',
    icon: Squares2X2Icon,
  },
  {
    name: 'Automations',
    description: 'Build strategic funnels that will drive your customers to convert',
    href: '#',
    icon: ArrowPathIcon,
  },
  {
    name: 'Reports',
    description: 'Get detailed reports that will help you make more informed decisions',
    href: '#',
    icon: DocumentChartBarIcon,
  },
]

const resources = [
  {
    name: 'Help Center',
    description: 'Get all of your questions answered in our forums or contact support.',
    href: '#',
  },
  { name: 'Guides', description: 'Learn how to maximize our platform to get the most out of it.', href: '#' },
  { name: 'Events', description: 'See what meet-ups and other events we might be planning near you.', href: '#' },
  { name: 'Security', description: 'Understand how we take your privacy seriously.', href: '#' },
]

export default function Example() {
  return (
    <Popover className="relative bg-white dark:bg-gray-900">
      <div className="flex items-center justify-between p-6 md:justify-start md:space-x-10">
        <div className="flex justify-start lg:w-0 lg:flex-1">
          <a href="#">
            <span className="sr-only">Your Company</span>
            <img
              alt=""
              src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600"
              className="h-8 w-auto dark:hidden sm:h-10"
            />
            <img
              alt=""
              src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500"
              className="hidden h-8 w-auto dark:block sm:h-10"
            />
          </a>
        </div>
        <div className="-my-2 -mr-2 md:hidden">
          <PopoverButton className="relative inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:ring-2 focus:ring-indigo-500 focus:outline-hidden focus:ring-inset dark:bg-gray-900 dark:hover:bg-white/5 dark:hover:text-gray-300">
            <span className="absolute -inset-0.5" />
            <span className="sr-only">Open menu</span>
            <Bars3Icon aria-hidden="true" className="size-6" />
          </PopoverButton>
        </div>
        <PopoverGroup as="nav" className="hidden space-x-10 md:flex">
          <Popover className="relative">
            <PopoverButton className="group inline-flex items-center rounded-md bg-white text-base font-medium text-gray-500 hover:text-gray-900 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-hidden data-open:text-gray-900 dark:bg-gray-900 dark:text-gray-300 dark:hover:text-white dark:data-open:text-white">
              <span>Solutions</span>
              <ChevronDownIcon
                aria-hidden="true"
                className="ml-2 size-5 text-gray-400 group-hover:text-gray-500 group-data-open:text-gray-600 group-data-open:group-hover:text-gray-500 dark:text-gray-500 dark:group-hover:text-gray-300 dark:group-data-open:text-gray-300"
              />
            </PopoverButton>

            <PopoverPanel
              transition
              className="absolute z-10 mt-3 -ml-4 w-screen max-w-md transform transition data-closed:translate-y-1 data-closed:opacity-0 data-enter:duration-200 data-enter:ease-out data-leave:duration-150 data-leave:ease-in lg:left-1/2 lg:ml-0 lg:max-w-2xl lg:-translate-x-1/2"
            >
              <div className="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5 dark:ring-white/10">
                <div className="relative grid gap-6 bg-white px-5 py-6 dark:bg-gray-900 sm:gap-8 sm:p-8 lg:grid-cols-2">
                  {solutions.map((solution) => (
                    <a
                      key={solution.name}
                      href={solution.href}
                      className="-m-3 flex items-start rounded-lg p-3 hover:bg-gray-50 dark:hover:bg-white/5"
                    >
                      <div className="flex size-10 shrink-0 items-center justify-center rounded-md bg-indigo-500 text-white sm:size-12">
                        <solution.icon aria-hidden="true" className="size-6" />
                      </div>
                      <div className="ml-4">
                        <p className="text-base font-medium text-gray-900 dark:text-white">{solution.name}</p>
                        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{solution.description}</p>
                      </div>
                    </a>
                  ))}
                </div>
                <div className="bg-gray-50 p-5 dark:bg-gray-800/50 sm:p-8">
                  <a href="#" className="-m-3 flow-root rounded-md p-3 hover:bg-gray-100 dark:hover:bg-white/5">
                    <div className="flex items-center">
                      <div className="text-base font-medium text-gray-900 dark:text-white">Enterprise</div>
                      <span className="ml-3 inline-flex items-center rounded-full bg-indigo-100 px-3 py-0.5 text-xs/5 font-medium text-indigo-800 dark:bg-indigo-500/20 dark:text-indigo-200">
                        New
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                      Empower your entire team with even more advanced tools.
                    </p>
                  </a>
                </div>
              </div>
            </PopoverPanel>
          </Popover>

          <a href="#" className="text-base font-medium text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
            Pricing
          </a>
          <a href="#" className="text-base font-medium text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
            Docs
          </a>

          <Popover className="relative">
            <PopoverButton className="group inline-flex items-center rounded-md bg-white text-base font-medium text-gray-500 hover:text-gray-900 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-hidden data-open:text-gray-900 dark:bg-gray-900 dark:text-gray-300 dark:hover:text-white dark:data-open:text-white">
              <span>More</span>
              <ChevronDownIcon
                aria-hidden="true"
                className="ml-2 size-5 text-gray-400 group-hover:text-gray-500 group-data-open:text-gray-600 group-data-open:group-hover:text-gray-500 dark:text-gray-500 dark:group-hover:text-gray-300 dark:group-data-open:text-gray-300"
              />
            </PopoverButton>

            <PopoverPanel
              transition
              className="absolute left-1/2 z-10 mt-3 w-screen max-w-xs -translate-x-1/2 transform px-2 transition data-closed:translate-y-1 data-closed:opacity-0 data-enter:duration-200 data-enter:ease-out data-leave:duration-150 data-leave:ease-in sm:px-0"
            >
              <div className="overflow-hidden rounded-lg shadow-lg ring-1 ring-black/5 dark:ring-white/10">
                <div className="relative grid gap-6 bg-white px-5 py-6 dark:bg-gray-900 sm:gap-8 sm:p-8">
                  {resources.map((resource) => (
                    <a
                      key={resource.name}
                      href={resource.href}
                      className="-m-3 block rounded-md p-3 hover:bg-gray-50 dark:hover:bg-white/5"
                    >
                      <p className="text-base font-medium text-gray-900 dark:text-white">{resource.name}</p>
                      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">{resource.description}</p>
                    </a>
                  ))}
                </div>
              </div>
            </PopoverPanel>
          </Popover>
        </PopoverGroup>
        <div className="hidden items-center justify-end md:flex md:flex-1 lg:w-0">
          <a href="#" className="text-base font-medium whitespace-nowrap text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
            Sign in
          </a>
          <a
            href="#"
            className="ml-8 inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium whitespace-nowrap text-white shadow-xs hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400"
          >
            Sign up
          </a>
        </div>
      </div>

      <PopoverPanel
        transition
        className="absolute inset-x-0 top-0 origin-top-right transform p-2 transition data-closed:scale-95 data-closed:opacity-0 data-enter:duration-200 data-enter:ease-out data-leave:duration-100 data-leave:ease-in md:hidden"
      >
        <div className="divide-y-2 divide-gray-50 rounded-lg bg-white shadow-lg ring-1 ring-black/5 dark:divide-white/10 dark:bg-gray-900 dark:ring-white/10">
          <div className="px-5 pt-5 pb-6">
            <div className="flex items-center justify-between">
              <div>
                <img
                  alt="Your Company"
                  src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600"
                  className="h-8 w-auto dark:hidden"
                />
                <img
                  alt="Your Company"
                  src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500"
                  className="hidden h-8 w-auto dark:block"
                />
              </div>
              <div className="-mr-2">
                <PopoverButton className="relative inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:ring-2 focus:ring-indigo-500 focus:outline-hidden focus:ring-inset dark:bg-gray-900 dark:hover:bg-white/5 dark:hover:text-gray-300">
                  <span className="absolute -inset-0.5" />
                  <span className="sr-only">Close menu</span>
                  <XMarkIcon aria-hidden="true" className="size-6" />
                </PopoverButton>
              </div>
            </div>
            <div className="mt-6">
              <nav className="grid grid-cols-1 gap-7">
                {solutions.map((solution) => (
                  <a
                    key={solution.name}
                    href={solution.href}
                    className="-m-3 flex items-center rounded-lg p-3 hover:bg-gray-50 dark:hover:bg-white/5"
                  >
                    <div className="flex size-10 shrink-0 items-center justify-center rounded-md bg-indigo-500 text-white">
                      <solution.icon aria-hidden="true" className="size-6" />
                    </div>
                    <div className="ml-4 text-base font-medium text-gray-900 dark:text-white">{solution.name}</div>
                  </a>
                ))}
              </nav>
            </div>
          </div>
          <div className="px-5 py-6">
            <div className="grid grid-cols-2 gap-4">
              <a href="#" className="text-base font-medium text-gray-900 hover:text-gray-700 dark:text-white dark:hover:text-gray-300">
                Pricing
              </a>

              <a href="#" className="text-base font-medium text-gray-900 hover:text-gray-700 dark:text-white dark:hover:text-gray-300">
                Docs
              </a>

              <a href="#" className="text-base font-medium text-gray-900 hover:text-gray-700 dark:text-white dark:hover:text-gray-300">
                Enterprise
              </a>
              {resources.map((resource) => (
                <a
                  key={resource.name}
                  href={resource.href}
                  className="text-base font-medium text-gray-900 hover:text-gray-700 dark:text-white dark:hover:text-gray-300"
                >
                  {resource.name}
                </a>
              ))}
            </div>
            <div className="mt-6">
              <a
                href="#"
                className="flex w-full items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium text-white shadow-xs hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400"
              >
                Sign up
              </a>
              <p className="mt-6 text-center text-base font-medium text-gray-500 dark:text-gray-400">
                Existing customer?{' '}
                <a href="#" className="text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300">
                  Sign in
                </a>
              </p>
            </div>
          </div>
        </div>
      </PopoverPanel>
    </Popover>
  )
}
