import os
import bibtexparser

### utility function ###

def keep_last_and_only(authors_str):
    """
    This function is dedicated to parse authors, it removes all the "and" but the last and and replace them with ", "
    :param str: string with authors
    :return: string with authors with only one "and"
    """

    last_author = authors_str.split(" and ")[-1]

    without_and = authors_str.replace(" and ", ", ")

    str_ok = without_and.replace(", " + last_author, " and " + last_author)

    return str_ok


def get_bibtex_line(filename, ID):
    start_line_number = 0
    end_line_number = 0

    with open(filename, encoding="utf-8") as myFile:
        for num, line in enumerate(myFile, 1):

            # first we look for the beginning line
            if start_line_number == 0:
                if (ID in line) and not ("@String" in line):
                    start_line_number = num
            else:  # after finding the start_line_number we go there
                # the last line contains "}"

                # we are at the next entry we stop here, end_line_number have the goof value
                if "@" in line:
                    assert end_line_number > 0
                    break

                if "}" in line:
                    end_line_number = num
    assert end_line_number > 0
    return start_line_number, end_line_number


def create_bib_link(ID):
    link = bibtex_filename
    start_bib, end_bib = get_bibtex_line(link, ID)

    # bibtex file is one folder upon markdown files
    #link = "../blob/master/" + link
    link += "#L" + str(start_bib) + "-L" + str(end_bib)

    # L66-L73
    return link


def get_md_entry(DB, entry, add_comments=True):
    """
    Generate a markdown line for a specific entry
    :param entry: entry dictionary
    :return: markdown string
    """
    md_str = ""

    if 'url' in entry.keys():
        md_str += "- [**" + entry['title'] + "**](" + entry['url'] + ") "
    else:
        md_str += "- **" + entry['title'] + "**"

    md_str += ", (" + entry['year'] + ")"

    md_str += " by *" + keep_last_and_only(entry['author']) + "*"

    md_str += " [[bib]](" + create_bib_link(entry['ID']) + ") "

    md_str += '\n'

    if add_comments:
        # maybe there is a comment to write
        if entry['ID'].lower() in DB.strings:
            #print("Com : " + entry['ID'])
            md_str += '``` \n'
            md_str += DB.strings[entry['ID'].lower()]
            md_str += '\n``` \n'

    return md_str


def get_md(DB, item, key, add_comments):
    """
    :param DB: list of dictionary with bibtex
    :param item: list of keywords to search in the DB
    :param key: key to use to search in the DB author/ID/year/keyword...
    :return: a md string with all entries corresponding to the item and keyword
    """

    all_str = ""

    list_entry = {}

    number_of_entries = len(DB.entries)
    for i in range(number_of_entries):
        if key in DB.entries[i].keys():
            if any(elem in DB.entries[i][key] for elem in item):
                str_md = get_md_entry(DB, DB.entries[i], add_comments)
                list_entry.update({str_md:DB.entries[i]['year']})


    sorted_tuple_list = sorted(list_entry.items(), reverse=True, key=lambda x: x[1])
    for elem in sorted_tuple_list:
        all_str += elem[0]

    return all_str


def get_outline(list_classif, filename):
    str_outline = "# Continual Learning Literature \n"

    str_outline += "This repository is maintained by Massimo Caccia and Timothée Lesort don't hesitate to send us an email to collaborate or fix some entries ({massimo.p.caccia , t.lesort} at gmail.com). The automation script of this repo is adapted from [Automatic_Awesome_Bibliography](https://github.com/TLESORT/Automatic_Awesome_Bibliography).\n\n For contributing to the repository please follow the process [here](https://github.com/optimass/continual_learning_papers/blob/master/scripts/README.md) \n\n"

    str_outline += "## Outline \n"

    for item in list_classif:
        str_outline += "- [" + item[0] + "](https://github.com/optimass/continual_learning_papers/blob/master/" + filename + "#" \
                       + item[0].replace(" ", "-").lower() + ')\n'

    return str_outline


def generate_md_file(DB, list_classif, key, plot_title_fct, filename, add_comments=True):
    """
    :param DB: list of dictionnary with bibtex
    :param list_classif: list with categories we want to put inside md file
    :param key: key allowing to search in the bibtex dictionary author/ID/year/keyword...
    :param plot_title_fct: function to plot category title
    :param filename: name of the markdown file
    :return: nothing
    """

    all_in_one_str = ""
    all_in_one_str += get_outline(list_classif, filename)

    for item in list_classif:

        str = get_md(DB, item, key, add_comments)

        if str != "":
            all_in_one_str += plot_title_fct(item)
            all_in_one_str += str

    f = open(filename, "w")
    f.write(all_in_one_str)
    f.close()

if __name__ == '__main__':
    bibtex_filename = "bibtex.bib"
    file_name = 'bibtex.bib'
    with open(file_name) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_db = bibtexparser.loads(bibtex_str, parser=bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False))

    ################################### Create Readme ####################################
    def plot_titles(titles):
        return '\n' + "## " + titles[0] + '\n'
"""
    list_types = [["Classics", "Classic"],
                ["Surveys", "Survey", "survey"],
                ["Influentials", "Influential"],
                ["New Settings or Metrics", "Setting", "Metric"],
                ["Regularization Methods", "Regularization"],
                ["Distillation Methods", "Distillation"],
                ["Rehearsal Methods", "Rehearsal"],
                ["Generative Replay Methods", "Generative Replay"],
                ["Dynamic Architectures or Routing Methods", "Architectures", "Dynamic Architecture"],
                ["Hybrid Methods", "Hybrid"],
                ["Continual Few-Shot Learning", "Continual-Meta Learning"],
                ["Meta-Continual Learning"],
                ["Lifelong Reinforcement Learning", "Reinforcement"],
                ["Continual Generative Modeling", "Generative Modeling"],
                ["Applications"],
                ["Thesis"],
                ["Workshops", 'Workshop']]
"""
    FEP_list_types = [["Surveys", "Survey"],
                ["Classics","classic"],
                ["Philosophical Analyses","philosophy"],
                ["Self-Organisation","self-organisation"],
                ["Information Geometry","information_geometry"]]
    AIF_list_types =[["Surveys and Tutorials","survey","tutorial"],
                    ["Discrete State Space Formulation","discrete"],
                    ["Continuous Time Formulation","continuous"],
                    ["Deep Active Inference", "deep"]]

    generate_md_file(DB=bib_db, list_classif=list_types, key="keywords", plot_title_fct=plot_titles, filename= "README.md", add_comments=True)