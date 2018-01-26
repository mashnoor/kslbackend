import json

import grequests

f = open("allitems.txt", "r")

items = json.load(f)
f.close()


def get_url(item_name):
    base_url = "http://www.dsebd.org/displayCompany.php?name="
    return base_url + item_name


all_links = []
all_items = []
for item in items:
    all_links.append(get_url(item["company"]))
    all_items.append(item["company"])

rs = (grequests.get(link) for link in all_links)

response_r = grequests.map(rs)

# get the responses
i = 0
for res in response_r:

    try:
        f = open("sources/" + all_items[i] + ".txt", "w+")
        f.write(res.content)
        f.close()

    except:
        print("Error :" + all_items[i])

    print(all_items[i])
    i += 1
    print (res.status_code)

