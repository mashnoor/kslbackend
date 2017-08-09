from bs4 import BeautifulSoup


def get_column_values(table, map_with):
    soup = BeautifulSoup(table, 'lxml')
    values = []

    for tr in soup.find_all("tr"):
        td = tr.find_all("td")[1]
        values.append(td.get_text().strip())

    return dict(zip(map_with, values))