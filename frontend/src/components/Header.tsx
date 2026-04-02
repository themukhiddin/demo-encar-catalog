export default function Header() {
  return (
    <header className="bg-white border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl font-bold tracking-tight">ENCAR</span>
          <span className="text-xl font-light text-gray-400">Catalog</span>
        </div>
        <nav className="hidden sm:flex items-center gap-6 text-sm font-medium text-gray-600">
          <a href="#cars" className="hover:text-black transition-colors">Cars</a>
          <a href="#" className="hover:text-black transition-colors">About</a>
        </nav>
      </div>
    </header>
  );
}
