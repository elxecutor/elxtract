import { useState } from "react";

export default function Header() {
  const [apiOpen, setApiOpen] = useState(false);
  return (
    <header className="flex justify-between items-center py-4 mx-8 md:mx-16 border-b-1 border-gray-400">
      <h1 className="text-2xl font-bold tracking-tight"><span className="text-(--accent)">el</span>xtract</h1>
      <nav>
        <ul className="flex items-center gap-6">
          <li className="relative">
            <button
              className="hover:text-(--accent) transition ease-in duration-300 font-medium focus:outline-none flex items-center"
              onClick={() => setApiOpen((v) => !v)}
              aria-expanded={apiOpen}
              aria-haspopup="true"
              type="button"
            >
              API
              <svg className={`inline ml-1 w-4 h-4 text-gray-500 transition ${apiOpen ? 'rotate-180 text-(--accent)' : 'group-hover:text-(--accent)'}`} fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" /></svg>
            </button>
            {apiOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-white border border-gray-200 rounded shadow-lg z-10 transition-opacity duration-200">
                <div className="p-4 text-sm text-gray-800">
                  <div className="mb-2 font-semibold text-gray-900">API Endpoints</div>
                  <ul className="mb-2 space-y-1">
                    <li><span className="font-mono text-xs">POST /api/formats/</span><br /><span className="text-xs text-gray-500">Get available formats for a YouTube URL</span></li>
                    <li><span className="font-mono text-xs">POST /api/download/</span><br /><span className="text-xs text-gray-500">Download a video in a selected format</span></li>
                  </ul>
                  <div className="font-semibold text-gray-900 mt-2">Example Request</div>
                  <pre className="bg-gray-100 rounded p-2 text-xs mt-1 overflow-x-auto">{`{
  "url": "https://youtube.com/watch?v=..."
}`}</pre>
                </div>
              </div>
            )}
          </li>
        </ul>
      </nav>
    </header>
  )
}