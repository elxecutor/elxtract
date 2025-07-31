import { useState } from "react";
export default function Body() {
    const [videoUrl, setVideoUrl] = useState("");
    return(
        <main>
            <section className="min-h-[50vh] p-8 py-24 flex flex-col gap-8 items-center">
                <h1 className="text-3xl">Youtube Video Downloader</h1>
                <div className="h-10 w-full max-w-[600px] flex items-center border-3 border-(--accent) rounded">
                    <input type="text" className="w-full bg-white h-full outline-none p-1" placeholder="Paste video link here" value={videoUrl} onChange={(e) => setVideoUrl(e.target.value)} />
                    <button className="bg-(--accent) text-white px-4 h-full cursor-pointer hover:contrast-125">Download</button>
                </div>
                <p className="text-sm font-100">By using our service you are accepting our <a href="" className="">Terms of Use</a></p>
            </section>
            <section className="p-8 py-16 flex flex-col md:flex-row gap-8 items-top">

                <img src="/assets/undraw_download_sa8g.svg" alt="" className="h-60 w-full md:w-1/2" />
                <div className="flex flex-col p-4 gap-4 w-full md:w-1/2">
                    <h2 className="text-2xl">How to download YouTube videos?</h2>
                    <ol>
                        <li>1. Visit <a href="https://www.youtube.com" className="">youtube.com</a> and find the specific video you want to save for offline use.</li>
                        <li>2. Copy the video URL from the address bar.</li>
                        <li>3. Paste the video URL into the input field above.</li>
                        <li>4. Click the "Download" button to start the process.</li>
                    </ol>
                </div>

            </section>
        </main>
    );
}