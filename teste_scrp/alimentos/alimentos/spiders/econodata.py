import scrapy


class EconodataSpider(scrapy.Spider):
    name = "econodata"

    # Lista de cidades e páginas
    cidades = ['itapeva', 'aracatuba', 'itapetininga', 'piracicaba', 'araraquara', 'ribeirao-preto', 'sao-jose-do-rio-preto']

    def start_requests(self):
        # Gera as URLs dinamicamente para todas as cidades e páginas
        for cidade in self.cidades:
            for num in range(1, 6):  # Paginação de 1 a 5
                url = f"https://www.econodata.com.br/maiores-empresas/sp-{cidade}/alimentos?pagina={num}"
                yield scrapy.Request(url=url, callback=self.parse, meta={'cidade': cidade, 'pagina': num})

    def parse(self, response):
        # Coleta as informações da página
        cidade = response.meta['cidade']
        pagina = response.meta['pagina']

        empresas = response.css('.block span::text').getall()
        ceps = response.css('.lg\:block::text').getall()
        setores = response.css('.max-w-2\.5xs::text').getall()

        # Gera uma linha separada para cada empresa
        for i in range(len(empresas)):
            yield {
                'cidade': cidade,
                'pagina': pagina,
                'empresa': empresas[i] if i < len(empresas) else None,
                'cep': ceps[i] if i < len(ceps) else None,
                'setor': setores[i] if i < len(setores) else None,
            }