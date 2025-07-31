import { useState } from "react";

function BodyComponent() {
    const [videoUrl, setVideoUrl] = useState("");
    const [formats, setFormats] = useState([]);
    const [loading, setLoading] = useState(false);
    const [downloading, setDownloading] = useState(false);
    const [error, setError] = useState("");
    const [downloadUrl, setDownloadUrl] = useState("");
    const [cleanupInfo, setCleanupInfo] = useState("");

    const fetchFormats = async () => {
        if (!videoUrl.trim()) {
            setError("Please enter a valid YouTube URL");
            return;
        }

        setLoading(true);
        setError("");
        setFormats([]);

        try {
            const response = await fetch('/api/formats/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: videoUrl }),
            });

            const data = await response.json();

            if (response.ok) {
                setFormats(data.formats);
                if (data.formats.length === 0) {
                    setError("No downloadable formats found for this video");
                }
            } else {
                setError(data.error || "Failed to fetch video formats");
            }
        } catch (err) {
            setError("Network error. Please check if the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    const downloadVideo = async (formatId) => {
        setDownloading(true);
        setError("");
        setDownloadUrl("");
        setCleanupInfo("");

        try {
            const response = await fetch('/api/download/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    url: videoUrl,
                    format_id: formatId
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setDownloadUrl(data.download_url);
                if (data.cleanup_info && data.cleanup_info.message) {
                    setCleanupInfo(data.cleanup_info.message);
                }
            } else {
                setError(data.error || "Failed to download video");
            }
        } catch (err) {
            setError("Network error. Please check if the backend is running.");
        } finally {
            setDownloading(false);
        }
    };

    const formatFileSize = (bytes) => {
        if (!bytes) return "Unknown size";
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    };

    return (
      <main>
        <section className="min-h-[50vh] p-8 py-24 flex flex-col gap-8 items-center">
          <h1 className="text-3xl">YouTube Video Downloader</h1>
          <div className="w-full max-w-[600px] flex flex-col gap-4">
            <div className="h-10 w-full flex items-center border-3 border-(--accent) rounded">
              <input
                type="text"
                className="w-full bg-white h-full outline-none p-1"
                placeholder="Paste video link or id here"
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && fetchFormats()}
              />
              <button
                className={`bg-(--accent) text-white h-full cursor-pointer hover:contrast-125 disabled:opacity-50 transition-all duration-200 whitespace-nowrap px-4`}
                onClick={fetchFormats}
                disabled={loading}
              >
                {loading ? "Getting Formats..." : "Get Format"}
              </button>
            </div>
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}
            {downloadUrl && (
              <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="flex flex-col items-start flex-1 min-w-0">
                  <p className="font-semibold truncate">Download ready!</p>
                  {cleanupInfo && (
                    <p className="text-sm mt-1 text-orange-600 truncate">
                      ℹ️ {cleanupInfo}
                    </p>
                  )}
                </div>
                <button
                  type="button"
                  className={`bg-(--accent) text-white px-4 py-2 rounded hover:contrast-125 disabled:opacity-50 cursor-pointer transition-all duration-200`}
                  onClick={async (e) => {
                    e.preventDefault();
                    try {
                      const response = await fetch(downloadUrl, {
                        credentials: "same-origin",
                      });
                      if (!response.ok) throw new Error("Failed to fetch file");
                      const blob = await response.blob();
                      const url = window.URL.createObjectURL(blob);
                      const link = document.createElement("a");
                      link.href = url;
                      // Try to extract filename from Content-Disposition header (RFC 6266)
                      const disposition = response.headers.get(
                        "Content-Disposition"
                      );
                      let filename = "";
                      if (disposition) {
                        // filename*=UTF-8''encoded-filename OR filename="quoted" OR filename=unquoted
                        const utf8Match = disposition.match(
                          /filename\*=UTF-8''([^;\n]+)/i
                        );
                        if (utf8Match) {
                          filename = decodeURIComponent(utf8Match[1]);
                        } else {
                          const filenameMatch = disposition.match(
                            /filename="?([^";\n]+)"?/i
                          );
                          if (filenameMatch) {
                            filename = filenameMatch[1];
                          }
                        }
                      }
                      // Fallback: try to extract from downloadUrl
                      if (!filename) {
                        try {
                          const urlParts = downloadUrl.split("/");
                          filename =
                            urlParts[urlParts.length - 1].split("?")[0] ||
                            "video";
                        } catch {
                          filename = "video";
                        }
                      }
                      link.setAttribute("download", filename);
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                      window.URL.revokeObjectURL(url);
                    } catch (err) {
                      alert("Failed to download file. Please try again.");
                    }
                  }}
                >
                  Download Video
                </button>
              </div>
            )}
            {formats.length > 0 && (
              <div className="w-full">
                <h3 className="text-lg font-semibold mb-4">
                  Available Formats:
                </h3>
                <div className="space-y-2">
                  {formats.map((format) => (
                    <div
                      key={format.format_id}
                      className="flex items-center justify-between p-3 border rounded hover:bg-gray-50"
                    >
                      <div className="flex-1">
                        <span className="font-medium">
                          {format.resolution
                            ? `${format.resolution}p`
                            : "Audio"}{" "}
                          ({format.ext})
                        </span>
                        {format.note && (
                          <span className="text-gray-600 ml-2">
                            - {format.note}
                          </span>
                        )}
                        {format.filesize && (
                          <div className="text-sm text-gray-500">
                            Size: {formatFileSize(format.filesize)}
                          </div>
                        )}
                      </div>
                      <button
                        onClick={() => downloadVideo(format.format_id)}
                        disabled={downloading}
                        className="bg-(--accent) text-white px-4 py-2 rounded hover:contrast-125 disabled:opacity-50 cursor-pointer transition-all duration-200"
                      >
                        {downloading ? "Downloading..." : "Download"}
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
          <p className="text-sm font-100">
            By using our service you are accepting our{" "}
            <a href="/terms" className="">
              Terms of Use
            </a>
          </p>
        </section>
        <section className="p-8 py-16 flex flex-col md:flex-row gap-8 items-top">
          <img
            src="/assets/undraw_download_sa8g.svg"
            alt=""
            className="h-60 w-full md:w-1/2"
          />
          <div className="flex flex-col p-4 gap-4 w-full md:w-1/2">
            <h2 className="text-2xl">How to download YouTube videos?</h2>
            <ol>
              <li>
                1. Visit{" "}
                <a href="https://www.youtube.com" className="">
                  youtube.com
                </a>{" "}
                and find the specific video you want to save for offline use.
              </li>
              <li>2. Copy the video URL from the address bar.</li>
              <li>3. Paste the video URL into the input field above.</li>
              <li>
                4. Click the "Get Format" button to see available download
                options.
              </li>
              <li>5. Choose your preferred format and click "Download".</li>
              <p className="text-sm text-gray-500 mt-2">
                <strong>Note:</strong> Downloaded files are automatically cleaned up to save space.
              </p>
            </ol>
            <div className="mt-4 p-3 bg-blue-50 rounded">
              <h3 className="font-semibold text-blue-800">Space Management</h3>
              <p className="text-sm text-blue-700">
                Files are automatically deleted after 24 hours to conserve
                server space.
              </p>
            </div>
          </div>
        </section>
      </main>
    );
}

// Error Boundary for fallback UI
import React from "react";
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }
    static getDerivedStateFromError(error) {
        return { hasError: true };
    }
    componentDidCatch(error, errorInfo) {
        // Optionally log error info
    }
    render() {
        if (this.state.hasError) {
            return <div style={{color: 'red', padding: '1em'}}>Something went wrong. Please reload the page.</div>;
        }
        return this.props.children;
    }
}

export default function Body(props) {
    return (
        <ErrorBoundary>
            <BodyComponent {...props} />
        </ErrorBoundary>
    );
}