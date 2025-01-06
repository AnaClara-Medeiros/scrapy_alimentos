import scrapy


class EconodataSpider(scrapy.Spider):
    name = "econodata"

    # Lista de cidades e páginas
    cidades = ['itapeva', 'aracatuba', 'itapetininga', 'piracicaba', 'araraquara', 'ribeirao-preto']

    def start_requests(self):
        # Gera as URLs dinamicamente para todas as cidades e páginas
        for cidade in self.cidades:
            for num in range(1, 6):  # Paginação de 1 a 5
                url = f"https://www.econodata.com.br/maiores-empresas/sp-{cidade}/alimentos?pagina={num}"
                yield scrapy.Request(url=url, callback=self.parse, meta={'cidade': cidade, 'pagina': num})

    def parse(self, response):
        # Coleta as informações da página
        qtd_empresas = response.css('#galhos-empresa-title-h1 .font-bold::text').get() 
        empresas = response.css('.block span::text').getall() 
        cidade = response.meta['cidade']  # Cidade enviada na meta
        pagina = response.meta['pagina']  # Página enviada na meta
        cep = response.css('.lg\:block::text').getall()
        setor = response.css('.max-w-2\.5xs::text').getall()

        # Retorna os resultados
        yield {
            'cidade': cidade,
            'pagina': pagina,
            'qtd_empresas': qtd_empresas,
            'empresas': empresas,
            'cep': cep,
            'setor': setor,
        }
