# Encar Catalog

Парсинг автомобилей с encar.com и отображение на лендинге.

## Стек

- **Backend**: Python 3.12, FastAPI, Playwright
- **Frontend**: Next.js, React, Tailwind CSS, TypeScript
- **DevOps**: Docker, Docker Compose

## Запуск через Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/cars

## Запуск локально

Backend:
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## API

- `GET /api/cars` - список автомобилей
- `POST /api/parse` - запустить парсинг

## Обновление данных

Парсинг запускается автоматически при старте, если данных нет. Для ежедневного обновления добавить cron на сервере:

```bash
crontab -e
```

```
0 3 * * * docker exec demo-encar-catalog-backend-1 curl -X POST http://localhost:8000/api/parse
```

Парсинг будет запускаться каждый день в 3:00.
