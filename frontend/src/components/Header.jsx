export default function Header() {
  return (
    <header className="flex justify-between items-center py-4 mx-8 md:mx-16 border-b-1 border-gray-400">
      <h1 className="text-2xl"><span className="text-(--accent)">el</span>xtract</h1>
      <nav>
        <ul>
          <li><a href="/" className="hover:text-(--accent) transition ease-in duration-300">API</a></li>
        </ul>
      </nav>
    </header>
  )
}