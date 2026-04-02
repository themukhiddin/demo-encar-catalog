from __future__ import annotations

import json
import os
import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright

DATA_PATH = Path(os.environ.get("DATA_PATH", Path(__file__).parent.parent / "data" / "cars.json"))

ENCAR_URL = (
    "https://www.encar.com/dc/dc_carsearchlist.do"
    "?carType=kor&searchType=model&pageCnt=50"
)


async def parse_cars(max_pages: int = 3) -> list[dict]:
    cars = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(ENCAR_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        for page_num in range(max_pages):
            items = await page.query_selector_all(".car_list li")

            for item in items:
                try:
                    car = await extract_car(item)
                    if car:
                        cars.append(car)
                except Exception:
                    continue

            if page_num < max_pages - 1:
                next_btn = await page.query_selector(".next")
                if next_btn:
                    await next_btn.click()
                    await page.wait_for_timeout(3000)
                else:
                    break

        await browser.close()

    return cars


async def extract_car(item) -> dict | None:
    # Фото
    img = await item.query_selector("img.thumb")
    if not img:
        return None

    photo = await img.get_attribute("src")
    if not photo or "transparent.gif" in photo:
        photo = await img.get_attribute("data-src")
    if not photo:
        return None
    if photo.startswith("//"):
        photo = "https:" + photo

    # Марка
    brand_el = await item.query_selector(".cls strong")
    brand = (await brand_el.inner_text()).strip() if brand_el else ""

    # Модель
    model_el = await item.query_selector(".cls em")
    model = (await model_el.inner_text()).strip() if model_el else ""

    # Детали модели
    detail_el = await item.query_selector(".dtl strong")
    detail = (await detail_el.inner_text()).strip() if detail_el else ""

    title = f"{brand} {model} {detail}".strip()

    # Год
    year_el = await item.query_selector(".yer")
    year_text = (await year_el.inner_text()).strip() if year_el else ""
    # Извлекаем год из формата "13/08식(14년형)" -> "2014"
    year_match = re.search(r"\((\d+)년형\)", year_text)
    if year_match:
        y = int(year_match.group(1))
        year = str(2000 + y) if y < 100 else str(y)
    else:
        # Берем первые цифры "13/08식" -> "2013"
        year_match2 = re.search(r"(\d+)/", year_text)
        if year_match2:
            y = int(year_match2.group(1))
            year = str(2000 + y) if y < 100 else str(y)
        else:
            year = year_text

    # Пробег
    km_el = await item.query_selector(".km")
    mileage = (await km_el.inner_text()).strip() if km_el else ""
    mileage = mileage.lstrip("· ").strip()

    # Цена
    price_el = await item.query_selector(".prc strong")
    price_num = (await price_el.inner_text()).strip() if price_el else ""
    price = f"{price_num}만원" if price_num else ""

    # ID для ссылки на encar
    link_el = await item.query_selector("a._link")
    href = await link_el.get_attribute("href") if link_el else ""
    car_id = ""
    if href:
        id_match = re.search(r"carid=(\d+)", href)
        car_id = id_match.group(1) if id_match else ""

    if not title or not price:
        return None

    return {
        "id": car_id,
        "brand": brand,
        "model": model,
        "title": title,
        "year": year,
        "mileage": mileage,
        "price": price,
        "photo": photo,
    }


def save_cars(cars: list[dict]):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)


def load_cars() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


async def run_scraper() -> list[dict]:
    cars = await parse_cars()
    save_cars(cars)
    return cars


if __name__ == "__main__":
    cars = asyncio.run(run_scraper())
    print(f"Scraped {len(cars)} cars")
    for car in cars[:5]:
        print(f"  {car['title']} | {car['year']} | {car['mileage']} | {car['price']}")
