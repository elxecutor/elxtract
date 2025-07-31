export default function Footer() {
  return (
    <footer className="flex flex-col md:flex-row items-center justify-between py-6 px-8 md:px-16 border-t border-gray-300 bg-gradient-to-t from-gray-50 to-white text-gray-700 mt-12">
      <div className="flex items-center gap-2 mb-2 md:mb-0">
        <span className="font-bold text-lg tracking-tight text-(--accent)">elxtract</span>
        <span className="text-xs text-gray-400">&copy; 2025</span>
      </div>
      <nav>
        <ul className="flex gap-6 text-sm">
          <li>
            <a
              href="/terms"
              className="hover:text-(--accent) underline underline-offset-4 transition-colors duration-200"
              target="_blank"
              rel="noopener noreferrer"
            >
              Terms of Service
            </a>
          </li>
        </ul>
      </nav>
    </footer>
  )
}