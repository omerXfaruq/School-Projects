import unittest
import json
import scholar_util

def isProfileCorrect():
    json = scholar_util.getUserProfileData(name="cemre")

    if json["id"] and "cemre" in json["name"].lower():
        return True
    else:
        return False

def author_citation(name):
    data = scholar_util.getAuthorCitationStats(name)
    data = dict(data["cites_per_year"])

    return data.get(2019)


def isGetAuthorsPublicationsCorrect():
    response = scholar_util.getAuthorsPublications("Ali")
    if response is not None:
        if response["publications"] is not None:
            isCorrect = True
            for publication in response["publications"]:
                isCorrect = (isCorrect
                             and type(publication["title"]) == str
                             and type(publication["author"]) == str
                             and type(publication["summary"]) == str
                             and type(publication["year"]) == str
                             and type(publication["url"]) == str)

    return isCorrect


def isSearchCorrect():
    json = scholar_util.searchPublication("cell")

    if 'FM Gill' not in json["author"]:
        return False
    else:
        return True


def isGetAuthorCorrect():
    for i in range(1, 10):
        json = scholar_util.getAuthors("Hawking", i)["author_search_result"]
        for author in json:
            if (author["name"] is None or
                    author["affiliation"] is None or
                    author["url_picture"] is None or
                    author["id"] is None):
                return False
        return True


class ScholarlyTest(unittest.TestCase):

    # Returns True or False.
    def test_author_publications(self):
        self.assertTrue(isGetAuthorsPublicationsCorrect() == True)

    def test_search(self):
        self.assertTrue(isSearchCorrect() == True)

    def test_profile_data(self):
        self.assertTrue(isProfileCorrect() == True)

    def test_get_author(self):
        self.assertTrue(isGetAuthorCorrect() == True)

    def test_author_citation_that_exists(self):
        can_kozcaz = 184

        self.assertEqual(author_citation("Can Kozcaz"), can_kozcaz)

    def test_author_citation_that_doesnt_exist(self):
        ibrahim_semiz = None

        self.assertEqual(author_citation("İbrahim Semiz"), ibrahim_semiz)

if __name__ == '__main__':
    unittest.main()
