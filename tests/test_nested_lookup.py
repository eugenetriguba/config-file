from unittest import TestCase

from config_file.nested_lookup import (
    get_all_keys,
    get_occurrence_of_key,
    get_occurrence_of_value,
    get_occurrences_and_values,
    nested_alter,
    nested_delete,
    nested_lookup,
    nested_update,
)


class TestNestedLookup(TestCase):
    def setUp(self):
        self.subject_dict = {"a": 1, "b": {"d": 100}, "c": {"d": 200}}
        self.subject_dict2 = {
            "name": "Russell Ballestrini",
            "email_address": "test1@example.com",
            "other": {
                "secondary_email": "test2@example.com",
                "EMAIL_RECOVERY": "test3@example.com",
                "email_address": "test4@example.com",
            },
        }
        self.subject_dict3 = {
            "build_version": {
                "model_name": "MacBook Pro",
                "build_version": {
                    "processor_name": "Intel Core i7",
                    "processor_speed": "2.7 GHz",
                    "core_details": {
                        "build_version": "4",
                        "l2_cache(per_core)": "256 KB",
                    },
                },
                "number_of_cores": "4",
                "memory": "256 KB",
            },
            "os_details": {"product_version": "10.13.6", "build_version": "17G65"},
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }
        self.subject_dict4 = {
            1: "a",
            2: {"b": 44, "C": 55},
            3: "d",
            4: "e",
            "6776": "works",
        }

    def test_nested_lookup(self):
        results = nested_lookup("d", self.subject_dict)
        self.assertEqual(2, len(results))
        self.assertIn(100, results)
        self.assertIn(200, results)
        self.assertSetEqual({100, 200}, set(results))

    def test_nested_lookup_wrapped_in_list(self):
        results = nested_lookup("d", [{}, self.subject_dict, {}])
        self.assertEqual(2, len(results))
        self.assertIn(100, results)
        self.assertIn(200, results)
        self.assertSetEqual({100, 200}, set(results))

    def test_nested_lookup_wrapped_in_list_in_dict_in_list(self):
        results = nested_lookup("d", [{}, {"H": [self.subject_dict]}])
        self.assertEqual(2, len(results))
        self.assertIn(100, results)
        self.assertIn(200, results)
        self.assertSetEqual({100, 200}, set(results))

    def test_nested_lookup_wrapped_in_list_in_list(self):
        results = nested_lookup("d", [{}, [self.subject_dict, {}]])
        self.assertEqual(2, len(results))
        self.assertIn(100, results)
        self.assertIn(200, results)
        self.assertSetEqual({100, 200}, set(results))

    def test_nested_lookup_key_is_non_str(self):
        results = nested_lookup(key=4, document=self.subject_dict4)
        self.assertIn("e", results)

    def test_wild_nested_lookup(self):
        results = nested_lookup(key="mail", document=self.subject_dict2, wild=True)
        self.assertEqual(4, len(results))
        self.assertIn("test1@example.com", results)
        self.assertIn("test2@example.com", results)
        self.assertIn("test3@example.com", results)

    def test_wild_nested_lookup_integer_keys_in_document(self):
        results = nested_lookup(key="c", document=self.subject_dict4, wild=True)
        self.assertIn(55, results)

    def test_wild_nested_lookup_integer_key_as_substring(self):
        # test that wild works converts integers into strings before substring matching.
        results = nested_lookup(key=77, document=self.subject_dict4, wild=True)
        self.assertIn("works", results)

    def test_wild_with_keys_nested_lookup(self):
        matches = nested_lookup(
            key="mail", document=self.subject_dict2, wild=True, with_keys=True
        )
        self.assertEqual(3, len(matches))
        self.assertIn("email_address", matches)
        self.assertIn("secondary_email", matches)
        self.assertIn("EMAIL_RECOVERY", matches)
        self.assertSetEqual(
            {"test1@example.com", "test4@example.com"}, set(matches["email_address"])
        )
        self.assertIn("test2@example.com", matches["secondary_email"])

    def test_nested_lookup_with_keys(self):
        matches = nested_lookup("d", self.subject_dict, with_keys=True)
        self.assertIn("d", matches)
        self.assertEqual(2, len(matches["d"]))
        self.assertSetEqual({100, 200}, set(matches["d"]))

    def test_after_key_is_found(self):
        result = nested_lookup(key="build_version", document=self.subject_dict3)
        self.assertEqual(4, len(result))
        self.assertIn("4", result)
        self.assertIn("17G65", result)
        match1 = {
            "processor_name": "Intel Core i7",
            "processor_speed": "2.7 GHz",
            "core_details": {"build_version": "4", "l2_cache(per_core)": "256 KB"},
        }
        self.assertIn(match1, result)
        match2 = {
            "build_version": {
                "processor_name": "Intel Core i7",
                "processor_speed": "2.7 GHz",
                "core_details": {"build_version": "4", "l2_cache(per_core)": "256 KB"},
            },
            "memory": "256 KB",
            "model_name": "MacBook Pro",
            "number_of_cores": "4",
        }
        self.assertIn(match2, result)


class TestGetAllKeys(TestCase):
    def setUp(self):
        self.sample1 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": {
                    "processor_name": "Intel Core i7",
                    "processor_speed": "2.7 GHz",
                    "core_details": {
                        "total_numberof_cores": "4",
                        "l2_cache(per_core)": "256 KB",
                    },
                },
                "total_number_of_cores": "4",
                "memory": "16 GB",
            },
            "os_details": {"product_version": "10.13.6", "build_version": "17G65"},
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }
        self.sample2 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": [
                    {
                        "processor_name": "Intel Core i7",
                        "processor_speed": "2.7 GHz",
                        "core_details": {
                            "total_numberof_cores": "4",
                            "l2_cache(per_core)": "256 KB",
                        },
                    }
                ],
                "total_number_of_cores": "4",
                "memory": "16 GB",
            }
        }
        self.sample3 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": [
                    {"processor_name": "Intel Core i7", "processor_speed": "2.7 GHz"},
                    {"total_numberof_cores": "4", "l2_cache(per_core)": "256 KB"},
                ],
                "total_number_of_cores": "4",
                "memory": "16 GB",
            }
        }
        self.sample4 = {
            "values": [
                {
                    "checks": [
                        {
                            "monitoring_zones": [
                                "mzdfw",
                                "mzfra",
                                "mzhkg",
                                "mziad",
                                "mzlon",
                                "mzord",
                                "mzsyd",
                            ]
                        }
                    ]
                }
            ]
        }
        self.sample5 = [
            {
                "listings": [
                    {
                        "name": "title",
                        "postcode": "postcode",
                        "full_address": "fulladdress",
                        "city": "city",
                        "lat": "latitude",
                        "lng": "longitude",
                    }
                ]
            }
        ]

    def test_sample_data1(self):
        result = get_all_keys(self.sample1)
        self.assertEqual(15, len(result))
        keys_to_verify = [
            "model_name",
            "core_details",
            "l2_cache(per_core)",
            "build_version",
            "date",
        ]
        for key in keys_to_verify:
            self.assertIn(key, result)

    def test_sample_data2(self):
        result = get_all_keys(self.sample2)
        self.assertEqual(10, len(result))
        keys_to_verify = [
            "hardware_details",
            "processor_speed",
            "total_numberof_cores",
            "memory",
        ]
        for key in keys_to_verify:
            self.assertIn(key, result)

    def test_sample_data3(self):
        result = get_all_keys(self.sample3)
        self.assertEqual(9, len(result))
        keys_to_verify = [
            "processor_details",
            "processor_name",
            "l2_cache(per_core)",
            "total_number_of_cores",
        ]
        for key in keys_to_verify:
            self.assertIn(key, result)

    def test_sample_data4(self):
        result = get_all_keys(self.sample4)
        self.assertEqual(3, len(result))
        keys_to_verify = ["values", "checks", "monitoring_zones"]
        for key in keys_to_verify:
            self.assertIn(key, result)

    def test_sample_data5(self):
        result = get_all_keys(self.sample5)
        self.assertEqual(7, len(result))
        keys_to_verify = [
            "listings",
            "name",
            "postcode",
            "full_address",
            "city",
            "lat",
            "lng",
        ]
        for key in keys_to_verify:
            self.assertIn(key, result)


class TestGetOccurrence(TestCase):
    def setUp(self):
        self.sample1 = {
            "build_version": {
                "model_name": "MacBook Pro",
                "build_version": {
                    "processor_name": "Intel Core i7",
                    "processor_speed": "2.7 GHz",
                    "core_details": {
                        "build_version": "4",
                        "l2_cache(per_core)": "256 KB",
                    },
                },
                "number_of_cores": "4",
                "memory": "256 KB",
            },
            "os_details": {"product_version": "10.13.6", "build_version": "17G65"},
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }
        self.sample2 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": [
                    {
                        "processor_name": "4",
                        "processor_speed": "2.7 GHz",
                        "core_details": {
                            "total_numberof_cores": "4",
                            "l2_cache(per_core)": "256 KB",
                        },
                    }
                ],
                "total_number_of_cores": "4",
                "memory": "16 GB",
            }
        }
        self.sample3 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": [
                    {"total_number_of_cores": "4", "processor_speed": "2.7 GHz"},
                    {"total_number_of_cores": "4", "l2_cache(per_core)": "256 KB"},
                ],
                "total_number_of_cores": "4",
                "memory": "16 GB",
            }
        }
        self.sample4 = {
            "values": [
                {
                    "checks": [
                        {
                            "monitoring_zones": [
                                "mzdfw",
                                "mzfra",
                                "mzhkg",
                                "mziad",
                                "mzlon",
                                "mzord",
                                "mzsyd",
                            ]
                        }
                    ]
                }
            ]
        }

        self.sample5 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "total_number_of_cores": 0,
                "memory": False,
            }
        }

        self.sample6 = [
            {
                "processor_name": "4",
                "processor_speed": "2.7 GHz",
                "core_details": {
                    "total_numberof_cores": "4",
                    "l2_cache(per_core)": "256 KB",
                },
            }
        ]

        self.sample7 = [
            {
                "processor_name": "4",
                "processor_speed": "2.7 GHz",
                "core_details": {
                    "total_numberof_cores": "4",
                    "l2_cache(per_core)": "256 KB",
                },
            },
            {
                "processor_name": "4",
                "processor_speed": "2.7 GHz",
                "core_details": {
                    "total_numberof_cores": "4",
                    "l2_cache(per_core)": "256 KB",
                },
            },
        ]

    def test_sample_data1(self):
        result = get_occurrence_of_key(self.sample1, "build_version")
        self.assertEqual(4, result)
        result = get_occurrence_of_value(self.sample1, "256 KB")
        self.assertEqual(2, result)

    def test_sample_data2(self):
        result = get_occurrence_of_key(self.sample2, "core_details")
        self.assertEqual(1, result)
        result = get_occurrence_of_value(self.sample2, "4")
        self.assertEqual(3, result)

    def test_sample_data3(self):
        result = get_occurrence_of_key(self.sample3, "total_number_of_cores")
        self.assertEqual(3, result)
        result = get_occurrence_of_value(self.sample3, "4")
        self.assertEqual(3, result)

    def test_sample_data4(self):
        result = get_occurrence_of_key(self.sample4, "checks")
        self.assertEqual(1, result)
        result = get_occurrence_of_value(self.sample4, "mziad")
        self.assertEqual(1, result)
        # Add one more value in key "monitoring_zones" and verify
        self.sample4["values"][0]["checks"][0]["monitoring_zones"].append("mziad")
        self.assertEqual(2, get_occurrence_of_value(self.sample4, "mziad"))

    def test_sample_data5(self):
        self.assertEqual(
            1, get_occurrence_of_key(self.sample5, "total_number_of_cores")
        )
        self.assertEqual(1, get_occurrence_of_key(self.sample5, "memory"))
        # Add key 'memory' and verify
        self.sample5["memory"] = 0
        self.assertEqual(2, get_occurrence_of_key(self.sample5, "memory"))

    def test_sample_data6(self):
        value = "4"
        result = get_occurrences_and_values(self.sample6, value)
        self.assertEqual(2, result[value]["occurrences"])
        self.assertEqual(2, len(result[value]["values"]))

    def test_sample_data7(self):
        value = "2.7 GHz"
        result = get_occurrences_and_values(self.sample6, value)
        self.assertEqual(1, result[value]["occurrences"])
        self.assertEqual(1, len(result[value]["values"]))

    def test_sample_data8(self):
        value = "4"
        result = get_occurrences_and_values(self.sample7, value)
        self.assertEqual(4, result[value]["occurrences"])
        self.assertEqual(4, len(result[value]["values"]))

    def test_sample_data9(self):
        value = "5"
        result = get_occurrences_and_values(self.sample7, value)
        self.assertEqual(0, result[value]["occurrences"])
        self.assertEqual(0, len(result[value]["values"]))


class BaseLookUpApi(TestCase):
    def setUp(self):
        self.sample_data1 = {
            "build_version": {
                "model_name": "MacBook Pro",
                "build_version": {
                    "processor_name": "Intel Core i7",
                    "processor_speed": "2.7 GHz",
                    "core_details": {
                        "build_version": "4",
                        "l2_cache(per_core)": "256 KB",
                    },
                },
                "number_of_cores": "4",
                "memory": "256 KB",
            },
            "os_details": {"product_version": "10.13.6", "build_version": "17G65"},
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }

        self.sample_data2 = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": [
                    {"processor_name": "Intel Core i7", "processor_speed": "2.7 GHz"},
                    {"total_number_of_cores": "4", "l2_cache(per_core)": "256 KB"},
                ],
                "total_number_of_cores": "5",
                "memory": "16 GB",
            }
        }

        self.sample_data3 = {
            "values": [
                {
                    "checks": [
                        {
                            "monitoring_zones": [
                                "mzdfw",
                                "mzfra",
                                "mzhkg",
                                "mziad",
                                "mzlon",
                                "mzord",
                                "mzsyd",
                            ]
                        }
                    ]
                }
            ]
        }

        self.sample_data4 = {
            "modelversion": "1.1.0",
            "vorgangsID": "1",
            "versorgungsvorschlagDatum": 1510558834978,
            "eingangsdatum": 1510558834978,
            "plz": 82269,
            "vertragsteile": [
                {
                    "typ": "1",
                    "beitragsDaten": {
                        "endalter": 85,
                        "brutto": 58.76,
                        "netto": 58.76,
                        "zahlungsrhythmus": "MONATLICH",
                        "plz": 86899,
                    },
                    "beginn": 1512082800000,
                    "lebenslang": "True",
                    "ueberschussverwendung": {
                        "ueberschussverwendung": "2",
                        "indexoption": "3",
                    },
                    "deckung": [
                        {
                            "typ": "2",
                            "art": "1",
                            "leistung": {"value": 7500242424.0, "einheit": "2"},
                            "leistungsRhythmus": "1",
                        }
                    ],
                    "zuschlagNachlass": [],
                },
                {
                    "typ": "1",
                    "beitragsDaten": {
                        "endalter": 85,
                        "brutto": 0.6,
                        "netto": 0.6,
                        "zahlungsrhythmus": "1",
                    },
                    "zuschlagNachlass": [],
                },
            ],
        }


class TestNestedDelete(BaseLookUpApi):
    def test_sample_data1(self):
        result = {
            "os_details": {"product_version": "10.13.6"},
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }
        self.assertEqual(result, nested_delete(self.sample_data1, "build_version"))

    def test_sample_data2(self):
        result = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "total_number_of_cores": "5",
                "memory": "16 GB",
            }
        }
        self.assertEqual(result, nested_delete(self.sample_data2, "processor_details"))

    def test_sample_data3(self):
        result = {"values": [{"checks": [{}]}]}
        self.assertEqual(result, nested_delete(self.sample_data3, "monitoring_zones"))


class TestNestedUpdate(BaseLookUpApi):
    def test_sample_data1(self):
        result = {
            "build_version": "Test1",
            "os_details": {"product_version": "10.13.6", "build_version": "Test1"},
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }
        self.assertEqual(
            result, nested_update(self.sample_data1, "build_version", "Test1")
        )

    def test_sample_data1_list_input_treat_list_as_element_true(self):
        result = {
            "build_version": ["Test5", "Test6", "Test7"],
            "os_details": {
                "product_version": "10.13.6",
                "build_version": ["Test5", "Test6", "Test7"],
            },
            "name": "Test",
            "date": "YYYY-MM-DD HH:MM:SS",
        }

        self.assertEqual(
            result,
            nested_update(
                self.sample_data1,
                "build_version",
                ["Test5", "Test6", "Test7"],
                treat_as_element=True,
            ),
        )

    def test_nested_update_in_place_false(self):
        """
        ested_update should mutate and return a copy of the original document
        """
        before_id = id(self.sample_data1)
        result = nested_update(
            self.sample_data1, "build_version", "Test2", in_place=False
        )
        after_id = id(result)
        # the object ids should _not_ match.
        self.assertNotEqual(before_id, after_id)

    def test_nested_update_in_place_true(self):
        """
        nested_update should mutate and return the original document
        """
        before_id = id(self.sample_data1)
        result = nested_update(
            self.sample_data1, "build_version", "Test2", in_place=True
        )
        after_id = id(result)
        # the object ids should match.
        self.assertEqual(before_id, after_id)

    def test_nested_update_in_place_true_list_input(self):
        doc = self.sample_data4
        # get all instances of the given element
        findings = nested_lookup("plz", doc, False, True)
        # alter those instances
        updated_findings = list()
        for key, val in findings.items():
            for elem in val:
                updated_findings.append(elem + 300)
        # update those instances with the altered results
        doc_updated = nested_update(
            doc, "plz", updated_findings, treat_as_element=False
        )
        elem1 = doc_updated["plz"]  # 85269
        # 87199
        elem2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        self.assertEqual(elem1, 82569)
        self.assertEqual(elem2, 87199)

    def test_nested_update_in_place_false_list_input(self):
        doc = self.sample_data4
        # get all instances of the given element
        findings = nested_lookup("plz", doc, False, True)
        # alter those instances
        updated_findings = list()
        for key, val in findings.items():
            for elem in val:
                updated_findings.append(elem + 300)
        # update those instances with the altered results
        doc_updated = nested_update(
            doc, "plz", updated_findings, in_place=False, treat_as_element=False
        )
        elem1 = doc_updated["plz"]
        elem2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        self.assertEqual(elem1, 82569)
        self.assertEqual(elem2, 87199)

    def test_nested_update_in_place_false_list_input_as_element_false(self):
        doc = self.sample_data4
        # get all instances of the given element
        list_input = [1, 2, 3, 4, 5]
        # update those instances with the altered results
        doc_updated = nested_update(
            doc, "plz", list_input, in_place=False, treat_as_element=False
        )
        elem1 = doc_updated["plz"]
        elem2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        # should not work without specifying "treat_list_as_element = True"
        # in nested_update
        self.assertNotEqual(elem1, list_input)
        self.assertNotEqual(elem2, list_input)

    def test_nested_update_in_place_false_list_input_as_element_true(self):
        doc = self.sample_data4
        # get all instances of the given element
        list_input = [1, 2, 3, 4, 5]
        # update those instances with the altered results
        doc_updated = nested_update(
            doc, "plz", list_input, in_place=False, treat_as_element=True
        )
        elem1 = doc_updated["plz"]
        elem2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        # should not work without specifying "treat_list_as_element = True"
        # in nested_update
        self.assertEqual(elem1, list_input)
        self.assertEqual(elem2, list_input)

    def test_nested_update_in_place_true_list_input_as_element_false(self):
        doc = self.sample_data4
        # get all instances of the given element
        list_input = [1, 2, 3, 4, 5]
        # update those instances with the altered results
        doc_updated = nested_update(
            doc, "plz", list_input, in_place=True, treat_as_element=False
        )
        elem1 = doc_updated["plz"]
        elem2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        # should not work without specifying "treat_list_as_element = True"
        # in nested_update
        self.assertNotEqual(elem1, list_input)
        self.assertNotEqual(elem2, list_input)

    def test_nested_update_in_place_true_list_input_as_element_true(self):
        doc = self.sample_data4
        # get all instances of the given element
        list_input = [1, 2, 3, 4, 5]
        # update those instances with the altered results
        doc_updated = nested_update(
            doc, "plz", list_input, in_place=True, treat_as_element=True
        )
        elem1 = doc_updated["plz"]
        elem2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        # should not work without specifying "treat_list_as_element = True"
        # in nested_update
        self.assertEqual(elem1, list_input)
        self.assertEqual(elem2, list_input)

    def test_nested_delete_in_place_false(self):
        """
        nested_delete should mutate and return a copy of the original document
        """
        before_id = id(self.sample_data1)
        result = nested_delete(self.sample_data1, "build_version", in_place=False)
        after_id = id(result)
        # the object ids should _not_ match.
        self.assertNotEqual(before_id, after_id)

    def test_nested_delete_in_place_true(self):
        """nested_delete should mutate and return the original document"""
        before_id = id(self.sample_data1)
        result = nested_delete(self.sample_data1, "build_version", in_place=True)
        after_id = id(result)
        # the object ids should match.
        self.assertEqual(before_id, after_id)

    def test_nested_update_taco_for_example(self):
        document = [{"taco": 42}, {"salsa": [{"burrito": {"taco": 69}}]}]

        updated_document = nested_update(
            document, "taco", [100, 200], treat_as_element=False
        )

        self.assertEqual(updated_document[0]["taco"], 100)
        # The multi-update version only works for scalar input,
        # if you need to adress a list of dicts, you have to
        # manually iterate over those and pass them to nested_update
        # one by one
        self.assertEqual(updated_document[1]["salsa"][0]["burrito"]["taco"], 200)

    def test_nested_update_raise_error(self):
        doc = self.sample_data4
        # get all instances of the given element
        list_input = 1
        # update those instances with the altered results
        self.assertRaises(
            Exception,
            nested_update,
            doc,
            "plz",
            list_input,
            in_place=True,
            treat_as_element=False,
        )

    def test_sample_data2(self):
        result = {
            "hardware_details": {
                "model_name": "MacBook Pro",
                "processor_details": {"test_key1": "test_value1"},
                "total_number_of_cores": "5",
                "memory": "16 GB",
            }
        }
        self.assertEqual(
            result,
            nested_update(
                self.sample_data2, "processor_details", {"test_key1": "test_value1"}
            ),
        )

    def test_sample_data3(self):
        result = {"values": [{"checks": {"key1": ["value1"], "key2": "value2"}}]}
        self.assertEqual(
            result,
            nested_update(
                self.sample_data3, "checks", {"key1": ["value1"], "key2": "value2"}
            ),
        )

    def test_sample_data4(self):
        result = {
            "modelversion": {"key1": ["value1"], "key2": "value2"},
            "vorgangsID": "1",
            "versorgungsvorschlagDatum": 1510558834978,
            "eingangsdatum": 1510558834978,
            "plz": 82269,
            "vertragsteile": [
                {
                    "typ": "1",
                    "beitragsDaten": {
                        "endalter": 85,
                        "brutto": 58.76,
                        "netto": 58.76,
                        "zahlungsrhythmus": "MONATLICH",
                        "plz": 86899,
                    },
                    "beginn": 1512082800000,
                    "lebenslang": "True",
                    "ueberschussverwendung": {
                        "ueberschussverwendung": "2",
                        "indexoption": "3",
                    },
                    "deckung": [
                        {
                            "typ": "2",
                            "art": "1",
                            "leistung": {"value": 7500242424.0, "einheit": "2"},
                            "leistungsRhythmus": "1",
                        }
                    ],
                    "zuschlagNachlass": [],
                },
                {
                    "typ": "1",
                    "beitragsDaten": {
                        "endalter": 85,
                        "brutto": 0.6,
                        "netto": 0.6,
                        "zahlungsrhythmus": "1",
                    },
                    "zuschlagNachlass": [],
                },
            ],
        }
        self.assertEqual(
            result,
            nested_update(
                self.sample_data4,
                "modelversion",
                {"key1": ["value1"], "key2": "value2"},
            ),
        )


class TestNestedAlter(BaseLookUpApi):
    def test_nested_alter_in_place_true(self):

        # callback functions
        def callback(data):
            return str(data) + "###"

        doc_updated = nested_alter(
            self.sample_data4, "vorgangsID", callback, in_place=True
        )

        vorgangsid = doc_updated["vorgangsID"]

        self.assertEqual(vorgangsid, "1###")

    def test_nested_alter_in_place_false(self):

        # callback functions
        def callback(data):
            return str(data) + "###"

        doc_updated = nested_alter(
            self.sample_data4, "vorgangsID", callback, in_place=False
        )

        vorgangsid = doc_updated["vorgangsID"]

        # should not work without specifying
        # "treat_list_as_element = True" in nested_update
        self.assertEqual(vorgangsid, "1###")

    def test_nested_alter_list_input_in_place_true(self):

        # callback functions
        def callback(data):
            return str(data) + "###"

        doc_updated = nested_alter(
            self.sample_data4, ["plz", "vorgangsID"], callback, in_place=True
        )

        plz1 = doc_updated["plz"]
        plz2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        vorgangsid = doc_updated["vorgangsID"]

        # should not work without specifying
        # "treat_list_as_element = True" in nested_update
        self.assertEqual(plz1, "82269###")
        self.assertEqual(plz2, "86899###")
        self.assertEqual(vorgangsid, "1###")

    def test_nested_alter_list_input_with_args_in_place_true(self):

        # callback functions
        def callback(data, str1, str2):
            return str(data) + str1 + str2

        doc_updated = nested_alter(
            self.sample_data4,
            ["plz", "vorgangsID"],
            callback,
            function_parameters=["abc", "def"],
            in_place=True,
        )

        plz1 = doc_updated["plz"]
        plz2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        vorgangsid = doc_updated["vorgangsID"]

        # should not work without specifying
        # "treat_list_as_element = True" in nested_update
        self.assertEqual(plz1, "82269abcdef")
        self.assertEqual(plz2, "86899abcdef")
        self.assertEqual(vorgangsid, "1abcdef")

    def test_nested_alter_list_input_with_args_in_place_false(self):

        # callback functions
        def callback(data, str1, str2):
            return str(data) + str1 + str2

        doc_updated = nested_alter(
            self.sample_data4,
            ["plz", "vorgangsID"],
            callback,
            function_parameters=["abc", "def"],
            in_place=False,
        )

        plz1 = doc_updated["plz"]
        plz2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        vorgangsid = doc_updated["vorgangsID"]

        # should not work without specifying
        # "treat_list_as_element = True" in nested_update
        self.assertEqual(plz1, "82269abcdef")
        self.assertEqual(plz2, "86899abcdef")
        self.assertEqual(vorgangsid, "1abcdef")

    def test_nested_alter_list_input_in_place_false(self):

        # callback functions
        def callback(data):
            return str(data) + "###"

        doc_updated = nested_alter(
            self.sample_data4, ["plz", "vorgangsID"], callback, in_place=False
        )

        plz1 = doc_updated["plz"]
        plz2 = doc_updated["vertragsteile"][0]["beitragsDaten"]["plz"]
        vorgangsid = doc_updated["vorgangsID"]

        # should not work without specifying
        # "treat_list_as_element = True" in nested_update
        self.assertEqual(plz1, "82269###")
        self.assertEqual(plz2, "86899###")
        self.assertEqual(vorgangsid, "1###")

    def test_nested_alter_taco_for_example(self):
        documents = [{"taco": 42}, {"salsa": [{"burrito": {"taco": 69}}]}]

        # write a callback function which processes a scalar value.
        # Be aware about the possible types which can be passed to
        # the callback functions.
        # In this example we can be sure that only int will be passed,
        # in production you should check the type because it could be
        # anything.
        def callback(data):
            return data + 10  # (data/100*10)

        # The alter-version only works for scalar input (one dict),
        # if you need to adress a list of dicts, you have to
        # manually iterate over those and pass them to
        # nested_update one by one
        out = []
        for elem in documents:
            altered_document = nested_alter(elem, "taco", callback)
            out.append(altered_document)

        self.maxDiff = None
        self.assertEqual(out[0]["taco"], 52)
        self.assertEqual(out[1]["salsa"][0]["burrito"]["taco"], 79)

    def test_nested_alter_work_with_right_order(self):
        document = {"taco": 42, "salsa": [{"burrito": {"key": 20}}], "key": 50}

        def callback(data):
            return data + 100

        altered_document = nested_alter(document, "key", callback, in_place=True)

        self.assertEqual(altered_document["salsa"][0]["burrito"]["key"], 120)
        self.assertEqual(altered_document["key"], 150)

    def test_sample_data4(self):

        result = {
            "modelversion": "1.1.0",
            "vorgangsID": "1",
            "versorgungsvorschlagDatum": 1510558834978,
            "eingangsdatum": 1510558834978,
            "plz": 82270,
            "vertragsteile": [
                {
                    "typ": "1",
                    "beitragsDaten": {
                        "endalter": 85,
                        "brutto": 58.76,
                        "netto": 58.76,
                        "zahlungsrhythmus": "MONATLICH",
                        "plz": 86900,
                    },
                    "beginn": 1512082800000,
                    "lebenslang": "True",
                    "ueberschussverwendung": {
                        "ueberschussverwendung": "2",
                        "indexoption": "3",
                    },
                    "deckung": [
                        {
                            "typ": "2",
                            "art": "1",
                            "leistung": {"value": 7500242424.0, "einheit": "2"},
                            "leistungsRhythmus": "1",
                        }
                    ],
                    "zuschlagNachlass": [],
                },
                {
                    "typ": "1",
                    "beitragsDaten": {
                        "endalter": 85,
                        "brutto": 0.6,
                        "netto": 0.6,
                        "zahlungsrhythmus": "1",
                    },
                    "zuschlagNachlass": [],
                },
            ],
        }

        # add +1 to all plz
        def callback(data):
            return data + 1

        self.maxDiff = None
        self.assertEqual(result, nested_alter(self.sample_data4, "plz", callback))
