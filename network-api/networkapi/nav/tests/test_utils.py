from unittest import TestCase

from networkapi.nav import utils


class TestUtils(TestCase):
    def test_nested_key_not_found(self):
        d = {"a": {"b": {"c": {"d": 1}}}}
        result = list(utils.find_key_values(d, "key"))
        self.assertEqual(result, [])

    def test_multiple_key_value_pairs(self):
        d = {"a": [1, 2, 3], "b": {"a": 4, "b": 5}, "c": [{"a": 6}, {"a": 7}]}
        result = list(utils.find_key_values(d, "a"))
        print(result)
        self.assertEqual(result, [[1, 2, 3], 4, 6, 7])

    def test_non_string_keys(self):
        d = {1: "a", 2: "b", 3: "c"}
        result = list(utils.find_key_values(d, 1))
        self.assertEqual(result, ["a"])

        # The function handles cases where the input dictionary contains non-hashable values.

    def test_non_hashable_values(self):
        d = {"a": [1, 2, 3], "b": {"c": [4, 5, 6]}, "d": 7}
        result = list(utils.find_key_values(d, "c"))
        expected = [[4, 5, 6]]
        self.assertEqual(result, expected)

    def test_extract_values_from_nested_dictionaries(self):
        d = {"id": 4, "a": {"id": 3, "b": {"id": 2, "c": {"id": 1}}}}
        result = list(utils.find_key_values(d, "id"))
        self.assertEqual(result, [4, 3, 2, 1])

    def test_dropdown_data(self):
        d = [
            {
                "type": "dropdown",
                "value": {
                    "title": "Girl pull.",
                    "overview": [],
                    "columns": [
                        {
                            "type": "item",
                            "value": {
                                "title": "Trial majority.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Hand think.",
                                            "description": "Remember media house hit point about.",
                                            "link_to": "page",
                                            "page": 586,
                                            "external_url": "https://mccann-patrick.com/",
                                            "relative_url": "",
                                        },
                                        "id": "d16bb637-347e-4a8c-98a0-7ee2346237fe",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Wait page land.",
                                            "description": "Increase important share it.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://dunn.info/",
                                            "relative_url": "",
                                        },
                                        "id": "e0b5f93d-e132-4078-9af0-5b303d52506e",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Wind notice.",
                                            "description": "Not respond able.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.anderson.com/",
                                            "relative_url": "",
                                        },
                                        "id": "d8d045f4-7f54-443f-927e-1af45ab99373",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Finally.",
                                            "description": "Next according hotel like environmental.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://tran.com/",
                                            "relative_url": "",
                                        },
                                        "id": "56874bfb-0124-43c4-8777-91bf246c0150",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Sound small form.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.moore.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c418a30f-688e-41d5-9510-cd10bdeff103",
                                    }
                                ],
                            },
                            "id": "dbac31df-453e-4fe6-856e-8acaca0cd0c7",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Be road recognize prevent.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Hospital loss.",
                                            "description": "Player a point friend tree half.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://riley-jimenez.com/",
                                            "relative_url": "",
                                        },
                                        "id": "013f34a0-c26f-4cc9-af78-451a40b1c2ea",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Century thought.",
                                            "description": "Big state paper young short purpose step.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://pratt.com/",
                                            "relative_url": "",
                                        },
                                        "id": "855b2128-1b60-4c4c-b4af-28cf1119dcc7",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Will standard physical cup.",
                                            "description": "Read raise ago point here road much.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://flores.com/",
                                            "relative_url": "",
                                        },
                                        "id": "63a84e95-cf1a-4a15-aa77-87d860ce01f9",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Both tree.",
                                            "description": "Spring within talk lot trade half.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.jones-santos.com/",
                                            "relative_url": "",
                                        },
                                        "id": "80c0fa41-41ea-4862-ab42-de99c1f5a84b",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Long leader travel.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.buck.info/",
                                            "relative_url": "",
                                        },
                                        "id": "e8ee7a09-1fe7-491e-bb80-120c78ba7234",
                                    }
                                ],
                            },
                            "id": "1f023bfd-5fa9-4b6a-bb98-29d7b2200610",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "To teacher.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Foot final maybe.",
                                            "description": "Sea idea difficult information day wrong later.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://larsen.com/",
                                            "relative_url": "",
                                        },
                                        "id": "cd7bd1e8-aebd-483a-ad02-7c9823b1e8dd",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Current study.",
                                            "description": "American share treat capital upon loss.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.williams-hood.com/",
                                            "relative_url": "",
                                        },
                                        "id": "8f761ac7-ecbb-4f8c-9ef2-3b2ac0b400d6",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Over politics another.",
                                            "description": "Operation unit spend two worry evidence employee particularly.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.harris.com/",
                                            "relative_url": "",
                                        },
                                        "id": "e4a2f3e0-c38a-441d-8f69-8266b69383af",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Late.",
                                            "description": "Myself writer major term deal none build.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.thomas-foster.info/",
                                            "relative_url": "",
                                        },
                                        "id": "00b0b045-451c-47d7-894f-2112d0c8dfc6",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Oil necessary edge.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.watson.com/",
                                            "relative_url": "",
                                        },
                                        "id": "be19ceb4-ece6-48b7-9973-59a893612512",
                                    }
                                ],
                            },
                            "id": "1f4397e3-3833-4d3a-99e2-261a0b4fb2ea",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Somebody hour hair.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Grow trial expect kind.",
                                            "description": "Indicate forward great raise many lawyer technology.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.williams-edwards.org/",
                                            "relative_url": "",
                                        },
                                        "id": "7120c834-6752-433a-882a-5c94446f702e",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Different future other.",
                                            "description": "Base yet girl green evidence.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://jimenez-vargas.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c6fa67c3-ccec-44b9-9146-2848c45449b1",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Involve successful blue.",
                                            "description": "Bed lay as.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://oconnell.org/",
                                            "relative_url": "",
                                        },
                                        "id": "d032696a-568f-4dbf-8668-efb27ad049e6",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Rest provide ten court.",
                                            "description": "Pressure lay material price.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.hill-mcdaniel.com/",
                                            "relative_url": "",
                                        },
                                        "id": "00ca47ff-cb79-4edb-b1fa-0d461f51bbcd",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Often technology.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.nicholson.com/",
                                            "relative_url": "",
                                        },
                                        "id": "cc2ff93f-d5e8-4689-a377-58bbe12fca88",
                                    }
                                ],
                            },
                            "id": "a9005a93-0a44-47c8-966b-9d9f166e24d2",
                        },
                    ],
                    "featured_column": [],
                    "button": [
                        {
                            "type": "item",
                            "value": {
                                "label": "Those.",
                                "link_to": "page",
                                "page": 587,
                                "external_url": "https://thomas.biz/",
                                "relative_url": "",
                            },
                            "id": "84356020-8d30-48e8-92e3-e803d195c4f3",
                        }
                    ],
                },
                "id": "1a393e7f-4586-4802-816e-f17aa6af9bc6",
            },
            {
                "type": "dropdown",
                "value": {
                    "title": "Lawyer.",
                    "overview": [],
                    "columns": [
                        {
                            "type": "item",
                            "value": {
                                "title": "Place church rate.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Manage century heavy since.",
                                            "description": "Unit across authority everything deal remain.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://davis.com/",
                                            "relative_url": "",
                                        },
                                        "id": "ffbe9f39-8aba-41b5-aa4e-5893ea4c93bc",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Edge nearly civil.",
                                            "description": "View teach body practice.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://huynh-farrell.net/",
                                            "relative_url": "",
                                        },
                                        "id": "3f0e4b8b-8637-4bb8-b6ff-3e42b6bb0c2e",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Three over image.",
                                            "description": "Mother decide certainly course behind during former.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://reed.com/",
                                            "relative_url": "",
                                        },
                                        "id": "980b86ae-8680-4a94-9f29-21b28616396c",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Management many.",
                                            "description": "So almost season entire its especially participant.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.green-williams.net/",
                                            "relative_url": "",
                                        },
                                        "id": "772917cb-7722-47f3-8210-a6ff78748062",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Someone couple us.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.smith.info/",
                                            "relative_url": "",
                                        },
                                        "id": "77aae307-acb0-438e-bd06-0579398fb193",
                                    }
                                ],
                            },
                            "id": "163f2dd0-737f-4032-8605-56c899dfe771",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Left fact.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Figure.",
                                            "description": "Many financial treatment to discuss now crime.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://glover.net/",
                                            "relative_url": "",
                                        },
                                        "id": "0ddd0e33-af3f-4928-959d-a444cc66d096",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Fire focus this.",
                                            "description": "Last beautiful look pick reflect week doctor.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://golden.com/",
                                            "relative_url": "",
                                        },
                                        "id": "7d8c56bb-6bb7-4eea-ad8b-b73a0ce2eddb",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Image city.",
                                            "description": "Become avoid end catch.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.lewis.com/",
                                            "relative_url": "",
                                        },
                                        "id": "ba9b6f1f-0b3c-459d-b349-0cd02050405b",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Itself business.",
                                            "description": "Director mouth spring politics community successful.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://diaz.com/",
                                            "relative_url": "",
                                        },
                                        "id": "d5309ff9-e935-4a1c-8f70-7017ab248961",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Kid evening tend.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://adams.com/",
                                            "relative_url": "",
                                        },
                                        "id": "7646360b-345b-4729-8856-f85f50c1373d",
                                    }
                                ],
                            },
                            "id": "954a14c8-770e-4a49-bb78-21decf88fc04",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Right but dark.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Order age.",
                                            "description": "Everybody professional must enough southern my manager.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.turner-jensen.info/",
                                            "relative_url": "",
                                        },
                                        "id": "d5dc89a2-15df-47dc-af7b-c2a846a7aa95",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Talk save.",
                                            "description": "Box book yes three when official already game.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.boyd.net/",
                                            "relative_url": "",
                                        },
                                        "id": "8001e903-3f67-41c7-8210-78036c4c907a",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Sort key economy.",
                                            "description": "Later huge authority hair ready sort either.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.garcia.info/",
                                            "relative_url": "",
                                        },
                                        "id": "4b64b22f-8f7f-4f9c-8fa2-7ea13a92776f",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Consider only save.",
                                            "description": "Happy cell note brother.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.roberts.com/",
                                            "relative_url": "",
                                        },
                                        "id": "41be888e-9d92-4511-ad10-ddcfee976835",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Blood whole let.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.roberts-lynch.com/",
                                            "relative_url": "",
                                        },
                                        "id": "4e121c81-152d-47f2-8fcb-1c8d65addc10",
                                    }
                                ],
                            },
                            "id": "318e3165-4cf4-42af-8c7b-0b35440056fc",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Like begin professor.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "This together at community.",
                                            "description": "Focus person full go cause group find.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.rodriguez.org/",
                                            "relative_url": "",
                                        },
                                        "id": "4e21f996-ef45-4412-b600-510f0c921d0e",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Dinner involve.",
                                            "description": "Support western wife personal letter.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.barton.biz/",
                                            "relative_url": "",
                                        },
                                        "id": "62431bdc-4bd6-4702-9ce4-7ef9c61b005f",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Member that.",
                                            "description": "Grow vote daughter radio.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.krause.com/",
                                            "relative_url": "",
                                        },
                                        "id": "33067f92-4854-4ef6-9c34-3956a1f2df32",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Allow director truth simple.",
                                            "description": "Able manage until eat participant true note.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://hamilton-knight.com/",
                                            "relative_url": "",
                                        },
                                        "id": "a03961a4-a790-497e-a0b1-2ae8a4723955",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Ahead father.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.robinson.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c8b8562b-8add-465a-b804-6bc91a5f2c36",
                                    }
                                ],
                            },
                            "id": "2979453f-a53a-42fb-8351-3536380f6d7c",
                        },
                    ],
                    "featured_column": [
                        {
                            "type": "item",
                            "value": {
                                "title": "Professional between.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Special opportunity although.",
                                            "icon": 1389,
                                            "link_to": "page",
                                            "page": 588,
                                            "external_url": "https://www.petty.info/",
                                            "relative_url": "",
                                        },
                                        "id": "55ca78c4-bf15-47f0-939e-3c3be974c7d3",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Room station whose interesting.",
                                            "icon": 1390,
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.sanders.com/",
                                            "relative_url": "",
                                        },
                                        "id": "3a6c6362-ebd1-4dc8-aa25-a3fbb511f33f",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Market.",
                                            "icon": 1391,
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://mckinney.info/",
                                            "relative_url": "",
                                        },
                                        "id": "f919b839-aa4b-48ac-b873-1d691b8f04ff",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Two key.",
                                            "icon": 1392,
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.greene-miller.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c1fce57b-90e0-4076-b656-4d86e6f8bc6d",
                                    },
                                ],
                            },
                            "id": "8f657565-a3ad-4766-80f8-a033f9d01d32",
                        }
                    ],
                    "button": [
                        {
                            "type": "item",
                            "value": {
                                "label": "Task particularly.",
                                "link_to": "external_url",
                                "page": None,
                                "external_url": "http://hernandez-collins.com/",
                                "relative_url": "",
                            },
                            "id": "9f3a5406-35b1-42b1-95b2-815e9fc0cd83",
                        }
                    ],
                },
                "id": "8f922ac3-77b7-49ea-9915-6078ea37ce6d",
            },
            {
                "type": "dropdown",
                "value": {
                    "title": "Trouble sea involve.",
                    "overview": [],
                    "columns": [
                        {
                            "type": "item",
                            "value": {
                                "title": "Consider party describe.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Open story travel.",
                                            "description": "Down condition professor include here no discover accept.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.willis.info/",
                                            "relative_url": "",
                                        },
                                        "id": "9b110b73-cd0f-46a1-826c-64bde2d5abde",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Upon she sure.",
                                            "description": "Each some own find yet.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://hernandez.net/",
                                            "relative_url": "",
                                        },
                                        "id": "eb8fa948-95b3-4dc9-82e3-ad1491fefa00",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Spend onto.",
                                            "description": "Capital lead anything audience.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.clarke-davidson.com/",
                                            "relative_url": "",
                                        },
                                        "id": "7f287dfd-d62b-4c5b-82e0-da56c3fcf640",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Minute poor.",
                                            "description": "Right heavy toward matter the game.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.smith.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c74b3d21-c315-4b66-ba30-e14c235b4638",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Away half.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.li-benson.info/",
                                            "relative_url": "",
                                        },
                                        "id": "9bb1de69-4c00-4562-9c29-5bfb6c8c56ac",
                                    }
                                ],
                            },
                            "id": "44d3713a-c7a1-409a-b4e9-d659b4d4df82",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Window.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Most difficult admit.",
                                            "description": "Poor really chance tree figure analysis.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.collins.biz/",
                                            "relative_url": "",
                                        },
                                        "id": "a2b14086-ce5a-4e3b-aa97-76d86dccaaca",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Day decision.",
                                            "description": "Half common education economy item others.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://miller.com/",
                                            "relative_url": "",
                                        },
                                        "id": "6213811b-0f56-43c6-965a-25313d88a7cc",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Dream feel.",
                                            "description": "Hold anyone leader structure common my education.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.smith.com/",
                                            "relative_url": "",
                                        },
                                        "id": "f90fb025-fa54-406e-a193-55117320ca6d",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Benefit side.",
                                            "description": "Experience fact hand share us.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.dixon.info/",
                                            "relative_url": "",
                                        },
                                        "id": "e3889144-f50a-4664-a0f5-77c50864479c",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Should leader may.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://hendrix.com/",
                                            "relative_url": "",
                                        },
                                        "id": "2ad35fbd-d327-45e4-a676-94f53851e024",
                                    }
                                ],
                            },
                            "id": "1ebe079b-f3f3-4a11-a83c-6a59f80edefb",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Inside easy.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Certainly wrong ten.",
                                            "description": "Until wide blood.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.gillespie.com/",
                                            "relative_url": "",
                                        },
                                        "id": "504883aa-f7e3-4933-aab2-ceed809da416",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Official all.",
                                            "description": "Firm final treat husband finally maintain drug.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.lopez.com/",
                                            "relative_url": "",
                                        },
                                        "id": "3f5f564c-a120-48c5-8f0a-e12f0a8439ef",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Way wide.",
                                            "description": "Point would such organization.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://palmer.biz/",
                                            "relative_url": "",
                                        },
                                        "id": "5f48a29f-1d76-43d3-af70-123a78b2628d",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Degree pressure open.",
                                            "description": "Stage thing game oil individual ability step result.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://murillo.com/",
                                            "relative_url": "",
                                        },
                                        "id": "603de901-7a58-4d6c-b690-76b133d6cab6",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Art home.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://jensen.biz/",
                                            "relative_url": "",
                                        },
                                        "id": "ec2eba6d-ea51-4fda-969e-e74142f85f86",
                                    }
                                ],
                            },
                            "id": "7ecf38dc-111d-4dcd-ab11-d66c1494ff2f",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Usually truth support.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Majority something crime.",
                                            "description": "Behind base behavior activity fall create.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.brooks.biz/",
                                            "relative_url": "",
                                        },
                                        "id": "5d655f88-fe56-48fb-9f74-a087435ddd12",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Attorney already represent.",
                                            "description": "Personal against table yourself.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://davenport.net/",
                                            "relative_url": "",
                                        },
                                        "id": "66cf9b07-38c9-45bf-b07d-d127fcd103dd",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Federal what kid.",
                                            "description": "Recognize never give though on player value.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://hogan.com/",
                                            "relative_url": "",
                                        },
                                        "id": "3f40c3b8-fbde-4835-abb5-c206265a41b6",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Public parent actually.",
                                            "description": "Protect on subject water.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.chang-willis.com/",
                                            "relative_url": "",
                                        },
                                        "id": "6d940dbb-d969-471c-bbd8-ca2a5ea97582",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Piece several.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.gates-lee.com/",
                                            "relative_url": "",
                                        },
                                        "id": "104c4433-66f2-4bc3-aa6a-7676b12ba1b4",
                                    }
                                ],
                            },
                            "id": "0475afa0-0b22-475a-85b9-c25157c06f3a",
                        },
                    ],
                    "featured_column": [],
                    "button": [
                        {
                            "type": "item",
                            "value": {
                                "label": "National goal.",
                                "link_to": "external_url",
                                "page": None,
                                "external_url": "http://www.sims.com/",
                                "relative_url": "",
                            },
                            "id": "4dbe719c-0a5e-4d7f-853f-9d463013e16f",
                        }
                    ],
                },
                "id": "8f4860f3-6e89-4917-8d8e-5b81c72432d3",
            },
            {
                "type": "dropdown",
                "value": {
                    "title": "Police.",
                    "overview": [],
                    "columns": [
                        {
                            "type": "item",
                            "value": {
                                "title": "Trouble.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Certainly least view.",
                                            "description": "Whether think economic city part he.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://parker.com/",
                                            "relative_url": "",
                                        },
                                        "id": "1273db47-e6e8-4870-8367-a83730faaae2",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Indeed field.",
                                            "description": "Use available recognize tend she guess avoid.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.cohen.com/",
                                            "relative_url": "",
                                        },
                                        "id": "61b54ed4-5533-4871-9c6a-6916e15d65fd",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "How ahead always.",
                                            "description": "Nation available design little partner.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.davis.net/",
                                            "relative_url": "",
                                        },
                                        "id": "8b6dc773-cca5-4992-abfc-5d5024369110",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "The chair professor.",
                                            "description": "Building lot service.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://hall.com/",
                                            "relative_url": "",
                                        },
                                        "id": "815f7ed5-c681-41f4-b54b-561ecc312e70",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Month hard although.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://henry.com/",
                                            "relative_url": "",
                                        },
                                        "id": "205a8f8b-6702-47db-a45d-e70e55e0207e",
                                    }
                                ],
                            },
                            "id": "714ac2a7-1335-45f6-98d6-d1dade85a4c5",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Business off game.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Few tend source.",
                                            "description": "Blood give return during.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://grant-freeman.com/",
                                            "relative_url": "",
                                        },
                                        "id": "24079532-70b2-4360-a38f-9eb6b2584952",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Customer front.",
                                            "description": "Western respond can clear.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.wallace.info/",
                                            "relative_url": "",
                                        },
                                        "id": "4b15ef67-5e11-403d-8f1a-e09067b86895",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Production your method.",
                                            "description": "Just step part.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.cook-wood.com/",
                                            "relative_url": "",
                                        },
                                        "id": "9cc4be30-95fe-4699-842e-0f1a8ca0672e",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Six around nor five.",
                                            "description": "Still establish machine write their charge.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://barnett.com/",
                                            "relative_url": "",
                                        },
                                        "id": "d02454a7-69cc-40c4-8cd9-2be960cc1756",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Represent clearly exist.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://mcdonald-thomas.biz/",
                                            "relative_url": "",
                                        },
                                        "id": "39df1ae4-1a01-41f8-a1da-bf66f1bddbc5",
                                    }
                                ],
                            },
                            "id": "eca145eb-b33d-470f-a2e6-8d435b523174",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Foot whom.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Gas quickly place.",
                                            "description": "Green doctor itself write notice.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://martinez.com/",
                                            "relative_url": "",
                                        },
                                        "id": "f54cc812-00a1-400f-a3cb-43371a6efe19",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Lawyer process.",
                                            "description": "Today radio that pull his course.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.logan-flores.org/",
                                            "relative_url": "",
                                        },
                                        "id": "5a51ab51-2e92-4ba4-9e91-706e74576587",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Value event serious.",
                                            "description": "The seek character cover college create.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.ramirez.com/",
                                            "relative_url": "",
                                        },
                                        "id": "7375343f-bc7a-4407-a249-c5f4048e6e0a",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Wish reach money approach.",
                                            "description": "Mrs agree usually of need term difficult.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://mccormick.com/",
                                            "relative_url": "",
                                        },
                                        "id": "9747c484-768d-44ef-8287-20afe9d70349",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Old.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.green.info/",
                                            "relative_url": "",
                                        },
                                        "id": "e89375e9-a459-4f50-a346-f25df97dacf7",
                                    }
                                ],
                            },
                            "id": "d11a92bc-41e2-4317-932c-c03702dd4157",
                        },
                        {
                            "type": "item",
                            "value": {
                                "title": "Writer wish.",
                                "nav_items": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Institution threat.",
                                            "description": "Threat everyone Mrs responsibility fish morning.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://mclean.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c9f78097-9f4e-474d-a564-adb89f992cef",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Sport rule four bank.",
                                            "description": "Sit data lead unit common among.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://gilbert.com/",
                                            "relative_url": "",
                                        },
                                        "id": "c283bcbc-af2a-4b09-98c2-ce357983b2f8",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Himself other so.",
                                            "description": "Recently suffer speak mouth care general sing speech.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "http://www.munoz-wilson.com/",
                                            "relative_url": "",
                                        },
                                        "id": "7a92a8d8-3d10-4a9d-a0f6-770931f609ca",
                                    },
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Clear finally point little.",
                                            "description": "Save without get exactly heart.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://www.bell.com/",
                                            "relative_url": "",
                                        },
                                        "id": "0047ab39-1f73-4407-91c7-2a35a30121a1",
                                    },
                                ],
                                "button": [
                                    {
                                        "type": "item",
                                        "value": {
                                            "label": "Wear third.",
                                            "link_to": "external_url",
                                            "page": None,
                                            "external_url": "https://shelton.info/",
                                            "relative_url": "",
                                        },
                                        "id": "d32546a5-d63d-4fbd-b5fe-417524a12bdf",
                                    }
                                ],
                            },
                            "id": "27f71330-0208-496f-917c-89be08d9375d",
                        },
                    ],
                    "featured_column": [],
                    "button": [
                        {
                            "type": "item",
                            "value": {
                                "label": "Back outside.",
                                "link_to": "external_url",
                                "page": None,
                                "external_url": "http://www.bush.info/",
                                "relative_url": "",
                            },
                            "id": "b3483367-f488-4f8f-ac41-dabc918eec56",
                        }
                    ],
                },
                "id": "b8694785-345f-4b0d-beea-a19ff7283222",
            },
        ]
        pages = []
        for dictionary in d:
            local_result = list(utils.find_key_values(dictionary, "page"))
            pages.extend(local_result)
        pages = [page for page in pages if page]
        expected = [586, 587, 588]
        self.assertEqual(pages, expected)
