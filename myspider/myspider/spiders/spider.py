import scrapy
from database import insert_product
from datetime import datetime


class PriceSpider(scrapy.Spider):
    name = 'price_spider'
    allowed_domains = ['amazon.fr']
    start_urls = [
        'https://www.amazon.fr/s?k=pc+portable&i=computers&rh=n%3A340858031%2Cp_n_feature_twenty-five_browse-bin%3A27399077031%2Cp_36%3A-50000&dc']

    def parse(self, response, **kwargs):
        products = response.css('div.s-main-slot div.s-result-item')

        for product in products:
            title = product.css('h2.a-size-mini a.a-link-normal span.a-text-normal::text').get()
            price = product.css('span.a-price-whole::text').get()
            link = product.css('h2.a-size-mini a.a-link-normal::attr(href)').get()

            if title and price:

                price = price.replace(' ', '').replace('\u202f', '')
                try:
                    price = float(price.replace(',', '.'))
                except ValueError:
                    self.logger.error(f"Erreur de conversion du prix: {price}")
                    price = None

                insert_product(
                    link=response.urljoin(link),
                    title=title,
                    price=price,
                    timestamp=datetime.utcnow().isoformat()
                )

        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
