import Image from "next/image";

interface Car {
  brand: string;
  model: string;
  title: string;
  year: string;
  mileage: string;
  price: string;
  photo: string;
}

export default function CarCard({ car }: { car: Car }) {
  return (
    <div className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-shadow duration-300">
      <div className="relative aspect-[4/3] bg-gray-100">
        <Image
          src={car.photo}
          alt={car.title}
          fill
          className="object-cover"
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        />
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-base truncate" title={car.title}>
          {car.title}
        </h3>
        <div className="flex items-center gap-3 mt-2 text-sm text-gray-500">
          {car.year && <span>{car.year}</span>}
          {car.year && car.mileage && <span className="w-1 h-1 rounded-full bg-gray-300" />}
          {car.mileage && <span>{car.mileage}</span>}
        </div>
        <div className="mt-3 flex items-center justify-between">
          <span className="text-lg font-bold">{car.price}</span>
          <a
            href={`https://www.encar.com`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-black text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors"
          >
            Details
          </a>
        </div>
      </div>
    </div>
  );
}
