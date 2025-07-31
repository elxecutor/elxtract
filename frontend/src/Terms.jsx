export default function Terms() {
  return (
    <main className="min-h-[60vh] flex flex-col items-center justify-center py-16 px-4 bg-gradient-to-b from-white to-gray-50 text-gray-800">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-md p-8 border border-gray-200">
        <h1 className="text-3xl font-bold mb-4 text-(--accent)">Terms of Service</h1>
        <p className="mb-4 text-gray-700">Welcome to elxtract! Please read these terms of service ("Terms", "Terms of Service") carefully before using our website and services.</p>
        <h2 className="text-xl font-semibold mt-6 mb-2">1. Acceptance of Terms</h2>
        <p className="mb-4">By accessing or using elxtract, you agree to be bound by these Terms. If you disagree with any part of the terms, you may not access the service.</p>
        <h2 className="text-xl font-semibold mt-6 mb-2">2. Use of Service</h2>
        <ul className="list-disc pl-6 mb-4 space-y-1">
          <li>You may use this service only for personal, non-commercial purposes.</li>
          <li>You are responsible for complying with all applicable laws regarding content downloading and copyright.</li>
          <li>We do not host any copyrighted content; all downloads are user-initiated and for personal use only.</li>
        </ul>
        <h2 className="text-xl font-semibold mt-6 mb-2">3. Disclaimer</h2>
        <p className="mb-4">elxtract is provided "as is" without warranties of any kind. We do not guarantee the accuracy, reliability, or availability of the service.</p>
        <h2 className="text-xl font-semibold mt-6 mb-2">4. Limitation of Liability</h2>
        <p className="mb-4">In no event shall elxtract or its owners be liable for any damages arising from the use or inability to use the service.</p>
        <h2 className="text-xl font-semibold mt-6 mb-2">5. Changes to Terms</h2>
        <p className="mb-4">We reserve the right to modify these Terms at any time. Changes will be posted on this page and your continued use of the service constitutes acceptance of those changes.</p>
        <p className="mt-8 text-sm text-gray-500">If you have any questions about these Terms, please contact us at support@elxtract.com.</p>
      </div>
    </main>
  );
}
