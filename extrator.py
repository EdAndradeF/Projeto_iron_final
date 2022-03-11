from datetime import datetime
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
from driver_chrome import Chrome
from backup import save
import selenium

#todo converter tudo para selenium
class DataSet:
    site = 'https://www.kaggle.com'

    def __init__(self, drive, ordem='hotness', pag=1):

        '''

        :param ordem: organiza os datasets pela ordem especicas
                    published: mais recentes
                    (default) hotness : relevancia
                    votes : mais votados
                    updated :  recente atualização
                    usability : usabilidade (ver criterios de usabilidade do Kaggle)

        :param pag: pagina para a pesquisa

        cria um objeto com a lista de URLs com repositorios de datasets do Kaggle apartir da configuração
        e organizaçao desejada
        '''

          # raiz
        self.secao = '/datasets'              # Secao de DataSets publicados no site
        self.ordem = f'sort={ordem}'          # ordenacao da lista
        self.pagina = f'page={pag}'           # pagina sendo respada
        self.url = f'{self.site}{self.secao}?{self.ordem}&{self.pagina}'
        print(self.url)
        self.driver = drive
        self.sopa = BeautifulSoup(self.driver.acessa(self.url, seg=0), 'lxml')

        self.href = self.links()                                                        # lista com as partes finais da urls das publicacoes
        self.posts_list = [Publica(x, self.driver) for x in tqdm(self.href, desc='PUBICACAO')]       # lista com dados de cada publicacao
        self.dataframe = pd.DataFrame(x.data for x in self.posts_list)
        self.date = datetime.today().date()
        self.dataframe.to_csv(f'data/dataset{self.secao}_{self.date}_{self.ordem}_{pag}.csv')



    def __repr__(self):
        return f'DataSet[{self.ordem}][{self.pagina}]'

    def links(self):
        tag_list = self.sopa.find('ul', 'km-list km-list--three-line').find_all('a', 'sc-eJocfa jARayQ')
        return [t.attrs['href'] for t in tag_list]



class Publica(DataSet):

    def __init__(self, url, drive):

        self.url = url
        self.post = f'{self.site}{url}'
        self.driver = drive.acessa(self.post,
                                   path='//*[@id="site-content"]/div[3]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/div/p')
        self.data = {}
        if self.driver:

            self.sopa = BeautifulSoup(self.driver, 'lxml')
            self.dataline()

            self.driver2 = drive.acessa(f'{self.post}/activity',
                                        path='//*[@id="site-content"]/div[3]/div[2]/div[1]/div[1]/div/div/div[1]/div[2]')
            self.sopa_act = BeautifulSoup(self.driver2, 'lxml')
            self.activety()

    def __repr__(self):
        return f'Publica<{self.post[22:]}>'

    def dataline(self):

        self.data['titulo'] = self.sopa.find('h1', {'class': 'dataset-header-v2__title'}).text
        self.data['autor'] = self.sopa.find('a', 'dataset-header-v2__owner-name').find('span').text
        self.data['dia'] = self.sopa.find('time').attrs['datetime'][4:15]
        self.data['horario'] = self.sopa.find('time').attrs['datetime'][16:24]
        self.data['usabilidade'] = self.sopa.find('p', {'data-test': 'rating'}).text
        self.data['licensa'] = self.sopa.find('a', {'target': '_blank'}).text
        texto = self.sopa.find('div', {'class': 'markdown-converter__text--rendered'})
        if texto:
            self.data['descricao'] = texto.text

        self.data['tags'] = self.sopa.find_all('div', {'class': 'mdc-menu-surface--anchor'})[1]

        #.text.split('Edit Tags')[0]  # todo precisa de tratamento
        if self.data['tags'].text.startswith('No tags yet'):
            self.data['tags'] = 'No tags yet'
        else:
            self.data['tags'] = [tag.text for tag in self.data['tags'].find_all('p')]
            self.data['tags'] = list(zip(self.data['tags'][0::2], self.data['tags'][1::2]))

        self.data['tamanho'] = self.sopa.find('div', {'data-testid': 'dataset-detail-render-tid'}).select('div:contains("Data Explorer")')
        self.data['tamanho'] = self.data['tamanho'][-1].find('p').text

        self.data['url'] = self.url


    def activety(self):

        body = self.sopa_act.find('div', {'id': 'site-content'}).find('div', {'data-testid': 'dataset-detail-render-tid'})

        lista_botvuca = ('Views', 'Upvote per Notebook Ratio', 'Upvote per post ratio')
        [self.minitab(body, x) for x in lista_botvuca]


        self.data['top_contributors'] = self.tabtab(body, 'Top contributors')

        self.data['top_complementary_datasets'] = self.tabtab(body, 'Top complementary datasets')


        self.data['notebook_ouro'] = body.find_all('span', {'type': 'gold'})[0].text
        self.data['notebook_prata'] = body.find_all('span', {'type': 'silver'})[0].text
        self.data['notebook_bronze'] = body.find_all('span', {'type': 'bronze'})[0].text



        self.data['discussao_ouro'] = body.find_all('span', {'type': 'gold'})[1].text
        self.data['discussao_prata'] = body.find_all('span', {'type': 'silver'})[1].text
        self.data['discussao_bronze'] = body.find_all('span', {'type': 'bronze'})[1].text



    def minitab(self, body, conts):
        tabs = body.select(f'div:contains("{conts}")')[-3].find_all('div')
        stats = [x.text for x in tabs[1:] if tabs.index(x) % 3]
        for ind in range(0, len(stats), 2):
            self.data[stats[ind + 1]] = stats[ind]

    def tabtab(self, body, conts):
        tabs = body.select(f'div:contains("{conts}")')[-1]
        se = tabs.find('ul')
        if not se:
            return tabs.find('div').text
        else:
            return [(c.find('a').attrs['href'], c.find_all('span')[1].text) for c in se.find_all('li')]



if __name__ == '__main__':



    d7 = DataSet('hotness')



    stap= 'dsfsdf'



