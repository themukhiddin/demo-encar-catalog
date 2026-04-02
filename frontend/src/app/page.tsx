import Header from "@/components/Header";
import CarCard from "@/components/CarCard";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Car {
  brand: string;
  model: string;
  title: string;
  year: string;
  mileage: string;
  price: string;
  photo: string;
}

async function getCars(): Promise<Car[]> {
  try {
    const res = await fetch(`${API_URL}/api/cars`, {
      next: { revalidate: 3600 },
    });
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export default async function Home() {
  const cars = await getCars();

  return (
    <>
      <Header />
      <main className="flex-1">
        {/* Hero */}
        <section className="bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
            <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">
              Korean Cars
            </h1>
            <p className="mt-2 text-gray-500 text-lg">
              Browse {cars.length > 0 ? cars.length : ""} vehicles from Encar.com
            </p>
          </div>
        </section>

        {/* Car Grid */}
        <section id="cars" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {cars.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {cars.map((car, i) => (
                <CarCard key={i} car={car} />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 text-gray-400">
              <p className="text-lg">No cars available yet</p>
              <p className="text-sm mt-1">Data is being parsed, check back soon</p>
            </div>
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-gray-400">
          Encar Catalog Demo &middot; Data from encar.com
        </div>
      </footer>
    </>
  );
}
