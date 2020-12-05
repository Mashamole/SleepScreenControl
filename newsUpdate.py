#!/usr/bin/env python
"""
Task: (Digital Reconaisance) || [ ReconDigital || DigiCon]
    1. Isolate data from each block of news (Check)
    2. find a way to search news blocks bases on zip code (In Progress)
        (-) Isolate search entry
    3. Create word search comparison and finder for
        handling words that are similiar.

    4. Check if its legal to scrape from other websites and use
        data in Web App.

    Goal:
        (+) Turn python app into Web application where I can input zip code or current location
            and it displays data on screen pertaining to location.

        (+) Expand app to Events occurring near location
"""
import urllib3
import requests
import re
import json
from bs4 import BeautifulSoup as soup


Headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    # # # # # # # # # # "cookie":"STYXKEY_PATCH_CONFIG=E9:c0; PATCH_SESSION=true; has_js=1; _igt=a8344a07-ab18-4d40-9c25-ffa1c867dfe1; _cmpQcif3pcsupported=1; p_usr_trkr={"val":4,"expiry":"Wed| 23 Dec 2020 03:37:35 GMT"}; _ig=7854447b-0f2b-4168-ebf1-cb912aa5a737",
    "if-none-match": "34f9d-81tK4xRciW/t1hwySAA1RKN+YGs",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41}"
}

CategoryList = {
    "Coronavirus": "covid-19",
    "arts-entertainment": "arts-entertainment",
    "business": "business",
    "around-town": "around-town",
    "police-fire": "police-fire",
    "lifestyle": "lifestyle",
    "going-green": "going-green",
    "kids-family": "kids-family",
    "obituaries": "obituaries",
    "personal-finance": "personal-finance",
    "pets": "pets",
    "politics": "politics",
    "restaurants-bars": "restaurants-bars",
    "schools": "schools",
    "sports": "sports",
    "traffic-transit": "traffic-transit",
    "travel": "travel",
    "weather": "weather"
}
# change location to current location


class DigitalRecon:

    RegionOfStateLinkUrl = []
    NearestRegionsByZip = {}
    State = "US"
    MainSite = "https://patch.com"

    def __init__(self, StateInput):
        self.State = StateInput

    def __init__(self):
        pass

    def setState(self, state):
        self.State = state

    def getState(self):
        return self.State

    def setUrl(self, url):
        self.MainSite = url

    def getUrl(self):
        return self.MainSite

    def getRegion(self, key):
        return self.NearestRegionsByZip[key][0], self.NearestRegionsByZip[key][1]

    def ZipCodeLocationSelect(self, zip):
        NearestTownsUrl = "https://patch.com/api_v1/patches.json?limit=8&query={0}&types[]=community&types[]=deals&types[]=national&types[]=seedling&types[]=smallBusiness&types[]=state".format(
            zip)
        http = urllib3.PoolManager()
        res = http.request("GET", NearestTownsUrl)
        JsonData = soup(res.data, 'lxml')
        townsNearYou = json.loads(JsonData.html.body.p.text)
        i = 1
        for town in townsNearYou:
            zipCodeLinks = []
            zipCodeLinks.append(town['name'])
            zipCodeLinks.append(town['alias'])
            self.setState(town['region']['name'])
            self.NearestRegionsByZip[i] = zipCodeLinks  # .append(town['name'])
            i += 1

    def UserRegion(self):

        selection = input("Select Region: ")
        while not selection.isdigit():
            selection = input("Select Region: ")
        region, RegionLink = self.getRegion(selection)

    def changeNewsLocation(self):
        location = self.State
        site = self.MainSite
        http = urllib3.PoolManager()
        res = http.request("GET", site)
        dataParse = soup(res.data, 'lxml')
        states = []
        # print(webSite + " " + location)
        stateSelection = dataParse.find_all(
            "a", class_="list-item__link list-item__link--xs")
        i = 1
        for state in stateSelection:
            # print(state.text)
            if i <= 52:
                states.append(state.text)
            i += 1

        statesMatch = dict(zip(states, states))
        if location == "District Of Columbia":
            location = "district-columbia/washingtondc"
            return site + "/" + location
        if location == "US":
            return site + "/" + "us" + "/" + "across-america"

        x = statesMatch[location].split(" ")
        state_encoder = "-".join(x)
        newSite = site + "/" + state_encoder
        # print(statesMatch)
        return newSite
        # print(newSite)

    def UrlModifierForRegionSelection(self, url):
        # check if url matches the state for modification
        # print(url)
        parsedUrl = url.split("/")
        # print(parsedUrl)
        if parsedUrl[len(parsedUrl) - 1] == 'washingtondc':
            del parsedUrl[len(parsedUrl) - 1]
            return url
        elif parsedUrl[len(parsedUrl) - 1] == "across-america":
            return url
        else:
            # print(parsedUrl)
            # modifiedUrl = "/".join(parsedUrl)
            # print(modifiedUrl)
            # print(url)
            return url

    def RegionSelection(self):

        # stateLocationUrl

        UrlModified = self.UrlModifierForRegionSelection(
            self.changeNewsLocation())
        http = urllib3.PoolManager()
        res = http.request("GET", UrlModified)
        dataParse = soup(res.data, 'lxml')
        stateURL = None
        # UrlModified = UrlModifierForRegionSelection(stateLocationUrl)
        for region in dataParse.find_all('li', class_="styles_CommunitiesBlock__listItem__3gMFv"):
            townLocation = region.find("href")
            self.RegionOfStateLinkUrl.append(
                [i for i in region.a.get("href").split("/")][2])
            stateURL = region.a.get("href").split("/")[1]
        # print(self.RegionOfStateLinkUrl) #list of all Regions in selected State
        # regionLink = UrlModified + "/" + \
        #     self.RegionOfStateLinkUrl[1]
        # print(regionLink)
        # return regionLink  # Select region from particular state

    def PrintRegionsNearZipCode(self):
        print(f"\nState: {self.getState()}")
        print("Regions in your Location:", '\n')
        for town in self.NearestRegionsByZip:
            print('\t', str(town) + ". " +
                  self.NearestRegionsByZip[town][0])
        print("\n")

    def deleteValues(self, array: list):
        array.clear()

    def NewsCategoriesSelect(self, selection):
        # changeNewsLocation(location=place)  # 'New Jersey')
        locationLink = self.MainSite
        # print(locationLink)
        topics = []
        http = urllib3.PoolManager()
        res = http.request("GET", locationLink, headers=Headers)
        parsedHtml = soup(res.data, 'lxml')

        # categories = parsedHtml.findAll()

        # print("{0}".format(CategoryList["business"]))

        CategoryLink = locationLink + "/" + \
            "{0}".format(CategoryList["business"])
        return CategoryLink
        # print(CategoryLink)
        # pattern = re.compile(r"")
        # href\=\"\\\w*\\\w*\\\")
        # i = 0
        # for tag in categories:
        #     print(tag.get("href"))
        # html = re.findall(pattern, str(tag))
        # for html in re.findall(pattern, str(tag)):
        #     print(html)

        # categories.find("li", class_="secondary-nav__menu-item")
        # print(categories)
        # i = 0
        # for title in categories:
        #     if i >= 131 and i <= 148:
        #         topics.append(title.text)
        #     i += 1
        # print(locationLink + "/" + "-".join(topics[2].split(" ")))

    def categoryLinksData(self):  # , link_site):
        link_site = self.MainSite  # NewsCategoriesSelect()
        http = urllib3.PoolManager()
        res = http.request("GET", link_site)
        dataParse = soup(res.data, 'lxml')
        print(link_site)

        """finds News Article headlines"""
        for tags in dataParse.find_all(
                "div", class_="styles_Card__TextContentWrapper__t8XqL styles_Card__TextContentWrapper--Condensed__1lJ_n"):
            tag = tags.find("h2")
            print(tag.text)

        """finds the time of News Article"""
        # for time_tag in dataParse.find_all("h6", class_="styles_Card__LabelWrapper__27yFr"):
        #     tg = time_tag.find("time")
        #     print(tg.text)

        """finds Description of News article"""
        # for tag_Description in dataParse.find_all(
        #         "div", class_="styles_Card__TextContentWrapper__t8XqL styles_Card__TextContentWrapper--Condensed__1lJ_n"):
        #     tagDesc = tag_Description.find("p")
        #     print(tagDesc.text, "\n")

    def wordComparison(self, locationWord):  # implement Trie class or function
        pass


"""
Simulate location selection and perform news finder based on location inserted
"""

# RegionSelection()


while True:
    try:
        digiCon = DigitalRecon()
        # print("Enter Current Location: ")
        # ("Enter Current State Location (eg) New York: ")
        userInput = input("Enter zip code or state: ")
        if userInput == "q" or userInput == "quit":
            break
        typeCheck = userInput.replace(" ", "")
        if typeCheck.isdigit():
            digiCon.ZipCodeLocationSelect(userInput)
            digiCon.PrintRegionsNearZipCode()
            # Make selection for regions nearby
        elif typeCheck.isalpha():  # call word comparison
            digiCon.setState(userInput)
            link = digiCon.changeNewsLocation()
            digiCon.setUrl(link)
            digiCon.RegionSelection()
            digiCon.categoryLinksData()
            print(digiCon.getUrl())
            print(digiCon.getState())
            # print(digiCon.RegionOfStateLinkUrl)
        else:
            print(
                f"Error invalid Input -> [ {userInput} ] (e.g., 08902, New York)")

        # ComparedWrd = wordComparison(userLocation) #Implement later
        # digiCon.setState(userLocation)
        # LocationUrl = digiCon.changeNewsLocation(location=userLocation)
        # digiCon.categoryLinksData(LocationUrl)
        # reg = digiCon.RegionSelection()
        # digiCon.PrintRegions()

    except ValueError as e:
        print(e.error)
