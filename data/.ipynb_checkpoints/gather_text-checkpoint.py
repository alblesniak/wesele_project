{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Pobranie tekstu oraz jego strukturyzacja do formatu JSON\n",
    "\n",
    "Poniższy notatnik prezentuje kod źródłowy skryptów napisanych w języku Python, które posłużyły do pobrania ze strony https://wolnelektury.pl tekstu dramatu autorstwa Stanisłwa Wyspiańskiego, pt.: _Wesele_. Tekst został następnie ustrukturyzowany w postaci słownika zawierającego dane dotyczące poszczególnych aktów i scen dramatu, wraz z podziałem dialogów na kwestie wypowiadane przez poszczególnych ich uczestników. Słownik został następnie przekonwertowany do formatu JSON oraz zapisany w postaci pliku `wesele-data.json`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "import re\n",
    "import requests\n",
    "import json\n",
    "import re"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "def roman_to_int(s):\n",
    "    '''Function transforming Roman numerals into Arabic'''\n",
    "    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n",
    "    int_val = 0\n",
    "    for i in range(len(s)):\n",
    "        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:\n",
    "            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]\n",
    "        else:\n",
    "            int_val += rom_val[s[i]]\n",
    "    return int_val"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "def make_soup(url, headers):\n",
    "    '''Function that returns an object BeautifulSoup'''\n",
    "    req = requests.get(wesele_url, headers=headers)\n",
    "    return BeautifulSoup(req.content, \"html5lib\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "wesele_url = 'https://wolnelektury.pl/katalog/lektura/wesele.html#anchor-idm140526473078944'\n",
    "headers = {\"User-Agent\" : \"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36\"}\n",
    "soup = make_soup(wesele_url, headers)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "author = soup.find(\"span\", {\"class\" : \"author\"}).get_text(strip=True)\n",
    "title = soup.find(\"span\", {\"class\" : \"title\"}).get_text(strip=True)\n",
    "subtitle = soup.find(\"span\", {\"class\" : \"subtitle\"}).get_text(strip=True)\n",
    "persons_list = []\n",
    "for div in soup.find_all(\"div\", {\"class\" : \"person-list\"}):\n",
    "    persons = [person.get_text(strip=True) for person in div.find_all(\"li\")]\n",
    "    persons_list.extend(persons)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "slideshow": {
     "slide_type": "-"
    }
   },
   "outputs": [],
   "source": [
    "main_text = soup.find(\"h3\", text=re.compile(\"DEKORACJA\")).find_next_siblings()\n",
    "text = []\n",
    "# dodanie do listy text wszystkich tagów, które nie są linkami (przypisami, numerami stron, etc.)\n",
    "for tag in main_text:\n",
    "    if tag.name != \"a\":\n",
    "        [a.extract() for a in tag(\"a\")]\n",
    "        [span.extract() for span in tag(\"span\")]\n",
    "        text.append(tag)\n",
    "        continue"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "decoration = \"\"\n",
    "for p in text:\n",
    "    p_text = p.get_text(strip=True)\n",
    "    if p_text.startswith(\"AKT I\"):\n",
    "        break\n",
    "    decoration += \"\\n\" + p_text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "persons_list = [] \n",
    "for div in soup.find_all(\"div\", {\"class\" : \"person-list\"}):\n",
    "    persons = [person.get_text(strip=True) for person in div.find_all(\"li\")]\n",
    "    persons_list.extend(persons)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "start_acts = []\n",
    "# pętla tworząca listę indeksów, od których rozpoczyna się każdy akt\n",
    "for index, tag in enumerate(text):\n",
    "    if tag.name == \"h2\":\n",
    "#         tag_text = tag.get_text(strip=True)\n",
    "#         act_number = roman_to_int(tag_text[4:])\n",
    "        start_acts.append(index)\n",
    "        continue\n",
    "    if tag.get(\"id\") == \"footnotes\":\n",
    "        last_index = index\n",
    "        continue"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "acts_indexes = []\n",
    "start_stop_tuple = ()\n",
    "# pętla tworząca listę krotek zawierających indeks początkowy i indeks końcowy aktów\n",
    "for i, start_index in enumerate(start_acts):\n",
    "    if i < len(start_acts) - 1:\n",
    "        start_stop_tuple += (start_index, start_acts[i + 1])\n",
    "        acts_indexes.append(start_stop_tuple)\n",
    "        start_stop_tuple = ()\n",
    "        continue\n",
    "    else:\n",
    "        start_stop_tuple += (start_index, last_index)\n",
    "        acts_indexes.append(start_stop_tuple)\n",
    "        del start_stop_tuple"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "acts_list_of_dicts = []\n",
    "acts = [text[start:stop] for (start, stop) in acts_indexes]\n",
    "\n",
    "for act in acts:\n",
    "\n",
    "    act_dict = {\n",
    "        \"Akt\" : None,\n",
    "        \"Didaskalia\" : None,\n",
    "        \"Sceny\" : []\n",
    "    }\n",
    "\n",
    "    # Flaga sprawdzająca czy didaskalia przyporządkowane są do aktu czy do sceny\n",
    "    inside_scene = False\n",
    "    # lista indeksów początkowych scen\n",
    "    start_scenes = []\n",
    "\n",
    "    for i, element in enumerate(act):\n",
    "\n",
    "        if element.name == \"h2\":\n",
    "            act_number = roman_to_int(element.get_text(strip=True)[4:])\n",
    "            act_dict[\"Akt\"] = act_number\n",
    "            continue\n",
    "        elif inside_scene == False and element.name == \"div\" and element[\"class\"][0] == \"didaskalia\":\n",
    "            act_dict[\"Didaskalia\"] = re.sub(re.compile(r\"\\s,\\s\"), \", \", element.get_text(strip=True, separator=\" \"))\n",
    "            continue\n",
    "        elif element.name == \"h3\":\n",
    "            inside_scene = True\n",
    "            start_scenes.append(i)  \n",
    "            \n",
    "            \n",
    "    for i, start_index in enumerate(start_scenes):\n",
    "        if i < len(start_scenes) - 1:\n",
    "            act_dict[\"Sceny\"].append(act[start_index:start_scenes[i+1]])\n",
    "            continue\n",
    "        else:\n",
    "            act_dict[\"Sceny\"].append(act[start_index:])\n",
    "    \n",
    "    acts_list_of_dicts.append(act_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "structured_text = []\n",
    "\n",
    "for act_element in range(len(acts_list_of_dicts)):\n",
    "    \n",
    "    # Skopiowanie struktury poprzedniej listy do nowej w celu nie ingerowania w iterowaną listę\n",
    "    act_dict = {\n",
    "        \"Akt\" : acts_list_of_dicts[act_element][\"Akt\"],\n",
    "        \"Didaskalia\" : acts_list_of_dicts[act_element][\"Didaskalia\"],\n",
    "        \"Sceny\" : []\n",
    "    }\n",
    "    structured_text.append(act_dict)\n",
    "    \n",
    "    for scene_element in range(len(acts_list_of_dicts[act_element])):\n",
    "        \n",
    "        for scene in acts_list_of_dicts[act_element][\"Sceny\"]:\n",
    "\n",
    "            scene_dict = {\n",
    "                \"Scena\" : None,\n",
    "                \"Didaskalia\" : [],\n",
    "                \"Dialog\" : []\n",
    "            }\n",
    "\n",
    "            for element in scene:\n",
    "            \n",
    "                if element.name == \"h3\":\n",
    "                    scene_number = roman_to_int(element.get_text(strip=True)[6:])\n",
    "                    scene_dict[\"Scena\"] = scene_number\n",
    "\n",
    "                elif element.name == \"div\" and element[\"class\"][0] == \"didaskalia\":\n",
    "                    scene_dict[\"Didaskalia\"].append(re.sub(re.compile(r\"\\s,\\s\"), \", \", element.get_text(strip=True, separator=\" \")))\n",
    "\n",
    "                elif element.name == \"h4\":\n",
    "                    person = element.get_text(strip=True)\n",
    "                    inside_dailog = True\n",
    "\n",
    "                elif element.name == \"div\" and element[\"class\"][0] == \"kwestia\":\n",
    "                    stanza = \"\\n\".join([p.get_text(strip=True, separator = \" \") for p in element.find(\"div\", {\"class\" : \"stanza\"}).find_all(\"p\", {\"class\" : \"verse\"})])\n",
    "\n",
    "                    dialog_dict = {\n",
    "                        \"Osoba\" : person,\n",
    "                        \"Zwrotka\" : stanza\n",
    "                    }\n",
    "\n",
    "                    scene_dict[\"Dialog\"].append(dialog_dict)\n",
    "            structured_text[act_element][\"Sceny\"].append(scene_dict)\n",
    "            "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "full_text = {\n",
    "    \"Autor\" : author,\n",
    "    \"Tytuł\" : title,\n",
    "    \"Podtytuł\" : subtitle,\n",
    "    \"Dekoracja\" : decoration,\n",
    "    \"Akty\" : structured_text\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "with open(\"wesele-data.json\", \"w\") as json_data:\n",
    "    json.dump(full_text, json_data, ensure_ascii=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 98,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 117,
   "metadata": {},
   "outputs": [],
   "source": [
    "for index, act in enumerate(full_text['Akty']):\n",
    "    for scene in act['Sceny']:\n",
    "        for dialog in scene['Dialog']:\n",
    "            name = dialog['Osoba'].lower().strip().replace(\" \", \"_\")\n",
    "            stanza = dialog['Zwrotka'].replace(r\"— — — — — — — — — — — —\", \"\").replace(\".  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .\", \"\") + \"\\n\"\n",
    "            if ',_' in name:\n",
    "                names = name.split(\",_\")\n",
    "                with open(\"stylo/corpus/\" + names[0] + \".txt\", \"a\") as file:\n",
    "                    file.write(stanza)\n",
    "                with open(\"stylo/corpus/\" + names[1] + \".txt\", \"a\") as file:\n",
    "                    file.write(stanza)\n",
    "            else:\n",
    "                with open('stylo/corpus/' + name + '.txt', 'a') as file:\n",
    "                    file.write(stanza)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
